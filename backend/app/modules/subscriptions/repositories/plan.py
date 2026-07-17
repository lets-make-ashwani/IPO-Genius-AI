from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.modules.subscriptions.models.plan import SubscriptionPlan, BillingInterval

class SubscriptionPlanRepository:
    def get_by_id(self, db: Session, plan_id: uuid.UUID) -> Optional[SubscriptionPlan]:
        return db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()

    def get_by_code(self, db: Session, code: str) -> Optional[SubscriptionPlan]:
        return db.query(SubscriptionPlan).filter(SubscriptionPlan.code == code).first()

    def list_active(self, db: Session) -> List[SubscriptionPlan]:
        return db.query(SubscriptionPlan).filter(SubscriptionPlan.is_active == True).all()

    def seed_default_plans(self, db: Session) -> None:
        """
        Seeds default subscription plans if the plans table is empty.
        """
        if db.query(SubscriptionPlan).count() > 0:
            return

        plans = [
            SubscriptionPlan(
                id=uuid.uuid4(),
                code="FREE",
                name="Free Plan",
                price_amount=0,
                currency="INR",
                billing_interval=BillingInterval.FREE,
                billing_interval_count=1,
                is_active=True
            ),
            SubscriptionPlan(
                id=uuid.uuid4(),
                code="PREMIUM_MONTHLY",
                name="Premium Monthly",
                price_amount=49900, # Rs. 499
                currency="INR",
                billing_interval=BillingInterval.MONTHLY,
                billing_interval_count=1,
                is_active=True
            ),
            SubscriptionPlan(
                id=uuid.uuid4(),
                code="PREMIUM_YEARLY",
                name="Premium Yearly",
                price_amount=499900, # Rs. 4999
                currency="INR",
                billing_interval=BillingInterval.YEARLY,
                billing_interval_count=1,
                is_active=True
            )
        ]

        db.bulk_save_objects(plans)
        db.commit()

plan_repository = SubscriptionPlanRepository()
