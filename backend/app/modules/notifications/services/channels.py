import logging
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.modules.notifications.models.notification import Notification, NotificationPreference

logger = logging.getLogger("app")

class BaseNotificationChannel(ABC):
    @abstractmethod
    def send(self, db: Session, notification: Notification, user_pref: NotificationPreference) -> bool:
        pass

class InAppChannel(BaseNotificationChannel):
    def send(self, db: Session, notification: Notification, user_pref: NotificationPreference) -> bool:
        if not user_pref.in_app_enabled:
            logger.info(f"InApp Channel disabled for user: {user_pref.user_id}")
            return False
            
        from app.modules.notifications.repositories.notification import notification_repository
        notification_repository.create(db, notification)
        logger.info(f"Persisted in-app notification: {notification.id} for user: {notification.user_id}")
        return True

class EmailChannel(BaseNotificationChannel):
    def send(self, db: Session, notification: Notification, user_pref: NotificationPreference) -> bool:
        # Delivery not implemented in this phase
        logger.info(f"[Email Channel Placeholder] Send notification '{notification.title}' to user {notification.user_id}")
        return True

class PushChannel(BaseNotificationChannel):
    def send(self, db: Session, notification: Notification, user_pref: NotificationPreference) -> bool:
        # Delivery not implemented in this phase
        logger.info(f"[Push Channel Placeholder] Send notification '{notification.title}' to user {notification.user_id}")
        return True

class TelegramChannel(BaseNotificationChannel):
    def send(self, db: Session, notification: Notification, user_pref: NotificationPreference) -> bool:
        # Delivery not implemented in this phase
        logger.info(f"[Telegram Channel Placeholder] Send notification '{notification.title}' to user {notification.user_id}")
        return True

class WhatsAppChannel(BaseNotificationChannel):
    def send(self, db: Session, notification: Notification, user_pref: NotificationPreference) -> bool:
        # Delivery not implemented in this phase
        logger.info(f"[WhatsApp Channel Placeholder] Send notification '{notification.title}' to user {notification.user_id}")
        return True
