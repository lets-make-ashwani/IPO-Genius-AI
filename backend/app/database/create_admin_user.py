"""
create_admin_user.py — Admin User Seeding Script

Creates a default administrator account in the database for admin console login.
"""

import uuid
import datetime
from app.database.session import SessionLocal
from app.modules.auth.models import RefreshToken  # Ensure model registered
from app.modules.watchlist.models import WatchlistFolder, WatchlistItem  # Ensure model registered
from app.modules.ipos.models.ipo import IPO  # Ensure model registered
from app.modules.ipos.models.detail import IPODetail  # Ensure model registered
from app.modules.ai.models.analysis import AIAnalysis  # Ensure model registered
from app.modules.notifications.models.notification import Notification, NotificationPreference  # Ensure model registered
from app.modules.subscriptions.models import UserSubscription  # Ensure model registered
from app.modules.users.models.user import User
from app.modules.auth.services import get_password_hash






def create_admin():
    db = SessionLocal()
    admin_email = "admin@ipogenius.ai"
    admin_pass = "Admin123456!"

    try:
        user = db.query(User).filter(User.email == admin_email).first()
        if user:
            user.role = "ADMIN"
            user.password_hash = get_password_hash(admin_pass)
            user.is_active = True
            db.commit()
            print(f"SUCCESS: Existing user '{admin_email}' updated to ADMIN role with password '{admin_pass}'.")
        else:
            new_admin = User(
                id=uuid.uuid4(),
                email=admin_email,
                password_hash=get_password_hash(admin_pass),
                full_name="System Administrator",
                role="ADMIN",
                is_active=True,
                created_at=datetime.datetime.now(datetime.timezone.utc),
                updated_at=datetime.datetime.now(datetime.timezone.utc)
            )
            db.add(new_admin)
            db.commit()
            print(f"SUCCESS: Created Admin user '{admin_email}' with password '{admin_pass}'.")

    except Exception as e:
        db.rollback()
        print(f"ERROR creating admin user: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
