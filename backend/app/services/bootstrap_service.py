"""
bootstrap_service.py — System Bootstrap Service

Provisions environment-driven Super Admin credentials and system default configurations.
"""

import uuid
import datetime
import logging
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.modules.auth.models import RefreshToken  # Ensure model registered
from app.modules.watchlist.models import WatchlistFolder, WatchlistItem  # Ensure model registered
from app.modules.ipos.models.ipo import IPO  # Ensure model registered
from app.modules.ipos.models.detail import IPODetail  # Ensure model registered
from app.modules.ai.models.analysis import AIAnalysis  # Ensure model registered
from app.modules.notifications.models.notification import Notification, NotificationPreference  # Ensure model registered
from app.modules.subscriptions.models import UserSubscription  # Ensure model registered
from app.modules.admin.models.system_metadata import SystemMetadata  # Ensure model registered
from app.modules.users.models.user import User
from app.modules.auth.services import get_password_hash

logger = logging.getLogger("app")

class BootstrapService:
    @staticmethod
    def ensure_super_admin(db: Session) -> User:
        """
        Ensures a Super Admin account exists in the database.
        Uses environment variables settings.SUPER_ADMIN_EMAIL and settings.SUPER_ADMIN_PASSWORD.
        """
        email = settings.SUPER_ADMIN_EMAIL
        password = settings.SUPER_ADMIN_PASSWORD
        name = settings.SUPER_ADMIN_NAME

        user = db.query(User).filter(User.email == email).first()
        if user:
            user.role = "ADMIN"
            user.password_hash = get_password_hash(password)
            user.is_active = True
            user.full_name = name
            logger.info(f"[Bootstrap] Super Admin '{email}' credentials updated.")
            return user
        else:
            admin_user = User(
                id=uuid.uuid4(),
                email=email,
                password_hash=get_password_hash(password),
                full_name=name,
                role="ADMIN",
                is_active=True,
                created_at=datetime.datetime.now(datetime.timezone.utc),
                updated_at=datetime.datetime.now(datetime.timezone.utc)
            )
            db.add(admin_user)
            logger.info(f"[Bootstrap] Created Super Admin '{email}'.")
            return admin_user
