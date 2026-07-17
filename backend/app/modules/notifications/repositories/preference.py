from sqlalchemy.orm import Session
from typing import Optional
import uuid
from datetime import datetime, timezone
from app.modules.notifications.models.notification import NotificationPreference

class NotificationPreferenceRepository:
    def get_by_user(self, db: Session, user_id: uuid.UUID) -> NotificationPreference:
        pref = (
            db.query(NotificationPreference)
            .filter(NotificationPreference.user_id == user_id)
            .first()
        )
        if not pref:
            pref = NotificationPreference(
                id=uuid.uuid4(),
                user_id=user_id,
                in_app_enabled=True,
                email_enabled=True,
                push_enabled=True,
                telegram_enabled=False,
                whatsapp_enabled=False,
                event_preferences={
                    "IPO_UPDATES": True,
                    "AI_ANALYSIS": True,
                    "WATCHLIST": True,
                    "SUBSCRIPTIONS": True,
                    "ADMIN_BROADCAST": True
                },
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            db.add(pref)
            db.commit()
            db.refresh(pref)
        return pref

    def update(self, db: Session, pref: NotificationPreference) -> NotificationPreference:
        db.commit()
        db.refresh(pref)
        return pref

preference_repository = NotificationPreferenceRepository()
