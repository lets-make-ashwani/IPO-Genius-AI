import logging
from sqlalchemy.orm import Session
import uuid
from typing import List, Tuple
from app.modules.notifications.models.notification import NotificationPreference, NotificationEventType
from app.modules.notifications.repositories.notification import notification_repository
from app.modules.notifications.repositories.preference import preference_repository

logger = logging.getLogger("app")

class RulesEngine:
    def evaluate(
        self,
        db: Session,
        user_id: uuid.UUID,
        event_type: NotificationEventType,
        context_metadata: dict = None,
        window_minutes: int = 5
    ) -> Tuple[bool, List[str]]:
        """
        Evaluates rules to determine if a notification should be created, and returns a list of target delivery channels.
        """
        # 1. Fetch user preferences
        pref = preference_repository.get_by_user(db, user_id)

        # 2. Check if event preference is enabled
        pref_key = self._get_preference_key(event_type)
        if pref_key:
            event_prefs = pref.event_preferences or {}
            if not event_prefs.get(pref_key, True):
                logger.info(f"Notification type {event_type} (key: {pref_key}) is disabled in preferences for user: {user_id}")
                return False, []

        # 3. Check for duplicate suppression (Rate limiting)
        # Prevent spamming duplicate notifications for the same user + event type + metadata within a short window
        if notification_repository.check_duplicate_exists(
            db, user_id=user_id, event_type=event_type, match_metadata=context_metadata, window_minutes=window_minutes
        ):
            logger.info(f"Duplicate notification suppressed for user {user_id}, event {event_type}")
            return False, []

        # 4. Resolve delivery channels
        channels = []
        if pref.in_app_enabled:
            channels.append("in_app")
        if pref.email_enabled:
            channels.append("email")
        if pref.push_enabled:
            channels.append("push")
        if pref.telegram_enabled:
            channels.append("telegram")
        if pref.whatsapp_enabled:
            channels.append("whatsapp")

        return True, channels

    def _get_preference_key(self, event_type: NotificationEventType) -> str | None:
        mapping = {
            NotificationEventType.IPO_STATUS_UPDATE: "IPO_UPDATES",
            NotificationEventType.IPO_OPEN: "IPO_UPDATES",
            NotificationEventType.IPO_CLOSE: "IPO_UPDATES",
            NotificationEventType.IPO_LISTED: "IPO_UPDATES",
            NotificationEventType.AI_ANALYSIS_COMPLETED: "AI_ANALYSIS",
            NotificationEventType.AI_ANALYSIS_UPDATED: "AI_ANALYSIS",
            NotificationEventType.WATCHLIST_ADDED: "WATCHLIST",
            NotificationEventType.WATCHLIST_REMINDER: "WATCHLIST",
            NotificationEventType.SUBSCRIPTION_UPDATED: "SUBSCRIPTIONS",
            NotificationEventType.PAYMENT_SUCCESS: "SUBSCRIPTIONS",
            NotificationEventType.PAYMENT_FAILED: "SUBSCRIPTIONS",
            NotificationEventType.ADMIN_BROADCAST: "ADMIN_BROADCAST",
            NotificationEventType.SYSTEM_NOTIFICATION: None
        }
        return mapping.get(event_type)

rules_engine = RulesEngine()
