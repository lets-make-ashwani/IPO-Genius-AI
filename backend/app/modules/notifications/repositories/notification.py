from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import Optional, List, Tuple
import uuid
from datetime import datetime, timezone, timedelta
from app.modules.notifications.models.notification import Notification, NotificationStatus

class NotificationRepository:
    def get_by_id(self, db: Session, notification_id: uuid.UUID) -> Optional[Notification]:
        return (
            db.query(Notification)
            .filter(Notification.id == notification_id, Notification.deleted_at == None)
            .first()
        )

    def list_by_user(
        self,
        db: Session,
        user_id: uuid.UUID,
        status_filter: Optional[NotificationStatus] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[Notification], int]:
        query = (
            db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.deleted_at == None)
        )
        if status_filter:
            query = query.filter(Notification.status == status_filter)
            
        query = query.order_by(desc(Notification.created_at))
        
        total = query.count()
        results = query.offset(offset).limit(limit).all()
        return results, total

    def count_unread(self, db: Session, user_id: uuid.UUID) -> int:
        return (
            db.query(func.count(Notification.id))
            .filter(
                Notification.user_id == user_id,
                Notification.status == NotificationStatus.UNREAD,
                Notification.deleted_at == None
            )
            .scalar() or 0
        )

    def create(self, db: Session, notification: Notification) -> Notification:
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    def update(self, db: Session, notification: Notification) -> Notification:
        db.commit()
        db.refresh(notification)
        return notification

    def soft_delete(self, db: Session, notification: Notification) -> Notification:
        notification.deleted_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(notification)
        return notification

    def mark_all_as_read(self, db: Session, user_id: uuid.UUID) -> int:
        rows_updated = (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.status == NotificationStatus.UNREAD,
                Notification.deleted_at == None
            )
            .update(
                {
                    Notification.status: NotificationStatus.READ,
                    Notification.is_read: True,
                    Notification.updated_at: datetime.now(timezone.utc)
                },
                synchronize_session=False
            )
        )
        db.commit()
        return rows_updated

    def check_duplicate_exists(
        self,
        db: Session,
        user_id: uuid.UUID,
        event_type: str,
        match_metadata: Optional[dict] = None,
        window_minutes: int = 5
    ) -> bool:
        time_cutoff = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
        query = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.event_type == event_type,
            Notification.created_at >= time_cutoff,
            Notification.deleted_at == None
        )
        
        if match_metadata:
            # For JSONB containment, we can fetch recent matching entries and inspect in python or use contains
            # Fetch last few entries to do exact key-value matching to be fully DB-implementation safe
            recent_items = query.order_by(desc(Notification.created_at)).limit(10).all()
            for item in recent_items:
                if item.context_metadata:
                    # check if all key-values in match_metadata are identical in context_metadata
                    match = True
                    for k, v in match_metadata.items():
                        if item.context_metadata.get(k) != v:
                            match = False
                            break
                    if match:
                        return True
            return False
            
        return query.count() > 0

notification_repository = NotificationRepository()
