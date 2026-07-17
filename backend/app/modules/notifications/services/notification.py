from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
import uuid
import logging
from datetime import datetime, timezone

from app.modules.notifications.models.notification import (
    Notification,
    NotificationPreference,
    NotificationEventType,
    NotificationPriority,
    NotificationStatus
)
from app.modules.notifications.repositories.notification import notification_repository
from app.modules.notifications.repositories.preference import preference_repository
from app.modules.notifications.services.rules import rules_engine
from app.modules.notifications.services.channels import (
    InAppChannel, EmailChannel, PushChannel, TelegramChannel, WhatsAppChannel
)
from app.modules.notifications.schemas.notification import NotificationPreferenceUpdate
from app.modules.users.repositories.activity import user_activity_repository
from app.shared.exceptions import AppException
from fastapi import status

logger = logging.getLogger("app")

class NotificationService:
    def __init__(self):
        # Instantiate Delivery Channels
        self.channels = {
            "in_app": InAppChannel(),
            "email": EmailChannel(),
            "push": PushChannel(),
            "telegram": TelegramChannel(),
            "whatsapp": WhatsAppChannel()
        }

    def create_notification(
        self,
        db: Session,
        user_id: uuid.UUID,
        title: str,
        message: str,
        event_type: NotificationEventType,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        context_metadata: Optional[dict] = None,
        action_label: Optional[str] = None,
        action_url: Optional[str] = None,
        expires_at: Optional[datetime] = None
    ) -> Optional[Notification]:
        # 1. Run Rules Engine checks
        should_send, target_channels = rules_engine.evaluate(
            db, user_id=user_id, event_type=event_type, context_metadata=context_metadata
        )
        if not should_send or not target_channels:
            return None

        # 2. Instantiate Model
        notification = Notification(
            id=uuid.uuid4(),
            user_id=user_id,
            title=title,
            message=message,
            event_type=event_type,
            priority=priority,
            status=NotificationStatus.UNREAD,
            is_read=False,
            context_metadata=context_metadata,
            action_label=action_label,
            action_url=action_url,
            expires_at=expires_at,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        user_pref = preference_repository.get_by_user(db, user_id)

        # 3. Dispatch to Channels
        dispatched_any = False
        for channel_name in target_channels:
            channel_impl = self.channels.get(channel_name)
            if channel_impl:
                try:
                    success = channel_impl.send(db, notification, user_pref)
                    if success and channel_name == "in_app":
                        dispatched_any = True
                except Exception as e:
                    logger.error(f"Error delivering channel {channel_name}: {str(e)}", exc_info=True)

        if not dispatched_any:
            logger.info("Notification rules evaluated true but in-app channel was disabled or delivery failed.")
            return None

        # 4. Log User Activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action="NOTIFICATION_CREATED",
            metadata_json={"notification_id": str(notification.id), "event_type": event_type.value}
        )

        return notification

    def list_notifications(
        self,
        db: Session,
        user_id: uuid.UUID,
        status_filter: Optional[NotificationStatus] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[Notification], int]:
        limit = min(max(limit, 1), 100)
        offset = max(offset, 0)
        return notification_repository.list_by_user(
            db, user_id=user_id, status_filter=status_filter, limit=limit, offset=offset
        )

    def get_unread_count(self, db: Session, user_id: uuid.UUID) -> int:
        return notification_repository.count_unread(db, user_id)

    def mark_as_read(self, db: Session, user_id: uuid.UUID, notification_id: uuid.UUID) -> Notification:
        notification = notification_repository.get_by_id(db, notification_id)
        if not notification:
            raise AppException("Notification not found", status_code=status.HTTP_404_NOT_FOUND)
        
        # Verify ownership
        if notification.user_id != user_id:
            raise AppException("Access denied: Not your notification", status_code=status.HTTP_403_FORBIDDEN)

        notification.status = NotificationStatus.READ
        notification.is_read = True
        notification.updated_at = datetime.now(timezone.utc)
        
        updated = notification_repository.update(db, notification)

        # Log Activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action="NOTIFICATION_READ",
            metadata_json={"notification_id": str(notification_id)}
        )
        return updated

    def mark_all_as_read(self, db: Session, user_id: uuid.UUID) -> int:
        rows = notification_repository.mark_all_as_read(db, user_id)
        
        # Log Activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action="NOTIFICATION_MARK_ALL_READ",
            metadata_json={"count_marked": rows}
        )
        return rows

    def get_preferences(self, db: Session, user_id: uuid.UUID) -> NotificationPreference:
        return preference_repository.get_by_user(db, user_id)

    def update_preferences(
        self, db: Session, user_id: uuid.UUID, update_in: NotificationPreferenceUpdate
    ) -> NotificationPreference:
        pref = preference_repository.get_by_user(db, user_id)

        if update_in.in_app_enabled is not None:
            pref.in_app_enabled = update_in.in_app_enabled
        if update_in.email_enabled is not None:
            pref.email_enabled = update_in.email_enabled
        if update_in.push_enabled is not None:
            pref.push_enabled = update_in.push_enabled
        if update_in.telegram_enabled is not None:
            pref.telegram_enabled = update_in.telegram_enabled
        if update_in.whatsapp_enabled is not None:
            pref.whatsapp_enabled = update_in.whatsapp_enabled
        if update_in.event_preferences is not None:
            # Merge or overwrite event preferences dictionary
            current_events = pref.event_preferences or {}
            current_events.update(update_in.event_preferences)
            pref.event_preferences = current_events

        pref.updated_at = datetime.now(timezone.utc)
        return preference_repository.update(db, pref)

notification_service = NotificationService()

# Subscribe NotificationService wrapper listener to decoupled EventDispatcher
from app.modules.notifications.events.dispatcher import event_dispatcher

def _notification_event_handler(
    db: Session,
    user_id: uuid.UUID,
    title: str,
    message: str,
    event_type: NotificationEventType,
    priority: NotificationPriority = NotificationPriority.NORMAL,
    context_metadata: Optional[dict] = None,
    action_label: Optional[str] = None,
    action_url: Optional[str] = None,
    expires_at: Optional[datetime] = None
):
    notification_service.create_notification(
        db=db,
        user_id=user_id,
        title=title,
        message=message,
        event_type=event_type,
        priority=priority,
        context_metadata=context_metadata,
        action_label=action_label,
        action_url=action_url,
        expires_at=expires_at
    )

event_dispatcher.subscribe("NOTIFICATION_TRIGGER", _notification_event_handler)
