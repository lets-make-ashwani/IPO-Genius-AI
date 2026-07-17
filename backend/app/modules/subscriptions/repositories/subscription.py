from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import uuid
import datetime
from app.modules.subscriptions.models.subscription import UserSubscription, SubscriptionStatus

class UserSubscriptionRepository:
    def get_by_id(self, db: Session, sub_id: uuid.UUID) -> Optional[UserSubscription]:
        return db.query(UserSubscription).filter(UserSubscription.id == sub_id).first()

    def get_active_subscription(self, db: Session, user_id: uuid.UUID, lock: bool = False) -> Optional[UserSubscription]:
        """
        Retrieves the user's currently active subscription.
        Optionally uses row-level write locking to prevent race conditions during updates.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        query = db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == SubscriptionStatus.ACTIVE,
            UserSubscription.end_date > now
        )
        if lock:
            query = query.with_for_update()
        return query.first()

    def get_any_active_or_pending(self, db: Session, user_id: uuid.UUID) -> List[UserSubscription]:
        """
        Retrieves any active or pending subscriptions.
        """
        return db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.PENDING])
        ).all()

    def create(self, db: Session, subscription: UserSubscription) -> UserSubscription:
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        return subscription

    def update(self, db: Session, subscription: UserSubscription) -> UserSubscription:
        db.commit()
        db.refresh(subscription)
        return subscription

    def list_all_paginated(self, db: Session, limit: int = 20, offset: int = 0) -> List[UserSubscription]:
        return db.query(UserSubscription).order_by(UserSubscription.created_at.desc()).offset(offset).limit(limit).all()

    def count_all(self, db: Session) -> int:
        return db.query(UserSubscription).count()

subscription_repository = UserSubscriptionRepository()
