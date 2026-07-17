from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
import datetime
import logging

from app.modules.subscriptions.models.subscription import UserSubscription, SubscriptionStatus
from app.modules.subscriptions.models.plan import SubscriptionPlan, BillingInterval
from app.modules.subscriptions.repositories.subscription import subscription_repository
from app.modules.subscriptions.repositories.plan import plan_repository
from app.modules.users.repositories.activity import user_activity_repository
from app.shared.exceptions import AppException
from app.modules.notifications.events.dispatcher import event_dispatcher
from fastapi import status

logger = logging.getLogger("app")

class UserSubscriptionService:
    def get_active_subscription(self, db: Session, user_id: uuid.UUID) -> Optional[UserSubscription]:
        return subscription_repository.get_active_subscription(db, user_id)

    def activate_subscription(self, db: Session, user_id: uuid.UUID, payment) -> UserSubscription:
        """
        Activates a subscription for the user, ensuring exactly one active subscription remains.
        """
        plan = plan_repository.get_by_id(db, payment.plan_id)
        if not plan:
            raise AppException("Plan not found", status_code=status.HTTP_404_NOT_FOUND)

        now = datetime.datetime.now(datetime.timezone.utc)

        # 1. Row lock check for existing active subscription
        active_sub = subscription_repository.get_active_subscription(db, user_id=user_id, lock=True)
        if active_sub:
            if payment.subscription_id == active_sub.id:
                logger.info(f"Subscription {active_sub.id} already activated for payment: {payment.id}")
                return active_sub

            # Transition existing active subscription to EXPIRED/CANCELLED to enforce single active rule
            logger.info(f"Deactivating existing subscription {active_sub.id} for user: {user_id}")
            active_sub.status = SubscriptionStatus.EXPIRED
            active_sub.end_date = now
            subscription_repository.update(db, active_sub)

        # 2. Compute billing interval period dates
        start_date = now
        if plan.billing_interval == BillingInterval.MONTHLY:
            end_date = start_date + datetime.timedelta(days=30 * plan.billing_interval_count)
        elif plan.billing_interval == BillingInterval.YEARLY:
            end_date = start_date + datetime.timedelta(days=365 * plan.billing_interval_count)
        else:
            # FREE or NONE - active for 100 years
            end_date = start_date + datetime.timedelta(days=36500)

        # 3. Create new user subscription
        subscription = UserSubscription(
            id=uuid.uuid4(),
            user_id=user_id,
            plan_id=plan.id,
            status=SubscriptionStatus.ACTIVE,
            start_date=start_date,
            end_date=end_date,
            cancel_at_period_end=False,
            provider_subscription_id=payment.provider_order_id,
            created_at=now,
            updated_at=now
        )

        created = subscription_repository.create(db, subscription)
        payment.subscription_id = created.id
        
        # Log activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action="SUBSCRIPTION_ACTIVATED",
            metadata_json={"subscription_id": str(created.id), "plan_code": plan.code}
        )

        # Dispatch decoupled event
        event_dispatcher.dispatch(
            "SUBSCRIPTION_UPDATED",
            db=db,
            user_id=user_id,
            subscription_id=created.id,
            status=SubscriptionStatus.ACTIVE.value
        )

        return created

    def cancel_subscription(self, db: Session, user_id: uuid.UUID) -> UserSubscription:
        """
        Sets cancel_at_period_end = True. User retains premium entitlement until end_date.
        """
        active_sub = subscription_repository.get_active_subscription(db, user_id=user_id, lock=True)
        if not active_sub:
            raise AppException("No active subscription found", status_code=status.HTTP_404_NOT_FOUND)

        if active_sub.cancel_at_period_end:
            return active_sub

        active_sub.cancel_at_period_end = True
        active_sub.status = SubscriptionStatus.CANCELLED
        active_sub.updated_at = datetime.datetime.now(datetime.timezone.utc)
        updated = subscription_repository.update(db, active_sub)

        # Log Activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action="SUBSCRIPTION_CANCELLED",
            metadata_json={"subscription_id": str(active_sub.id)}
        )

        # Dispatch Event
        event_dispatcher.dispatch(
            "SUBSCRIPTION_UPDATED",
            db=db,
            user_id=user_id,
            subscription_id=active_sub.id,
            status=SubscriptionStatus.CANCELLED.value
        )

        return updated

    def expire_outdated_subscriptions(self, db: Session) -> int:
        """
        Finds all active/cancelled subscriptions whose end_date has passed, and transitions them to EXPIRED.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        expired_count = 0

        # Query all active or cancelled subscriptions whose end_date <= now
        outdated = db.query(UserSubscription).filter(
            UserSubscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.CANCELLED]),
            UserSubscription.end_date <= now
        ).all()

        for sub in outdated:
            sub.status = SubscriptionStatus.EXPIRED
            sub.updated_at = now
            subscription_repository.update(db, sub)
            expired_count += 1

            # Log Activity
            user_activity_repository.log_activity(
                db,
                user_id=sub.user_id,
                action="SUBSCRIPTION_EXPIRED",
                metadata_json={"subscription_id": str(sub.id)}
            )

            # Dispatch Event
            event_dispatcher.dispatch(
                "SUBSCRIPTION_UPDATED",
                db=db,
                user_id=sub.user_id,
                subscription_id=sub.id,
                status=SubscriptionStatus.EXPIRED.value
            )

        return expired_count

subscription_service = UserSubscriptionService()
