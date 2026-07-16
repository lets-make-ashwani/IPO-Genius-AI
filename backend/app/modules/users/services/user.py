import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile, status

from app.modules.users.models.user import User
from app.modules.users.models.settings import UserSetting
from app.modules.users.models.activity import UserActivity, UserActivityType
from app.modules.users.schemas.user import ChangePasswordRequest, UserUpdate
from app.modules.users.schemas.settings import UserSettingUpdate
from app.modules.users.repositories.user import user_repository
from app.modules.users.repositories.settings import user_setting_repository
from app.modules.users.repositories.activity import user_activity_repository
from app.modules.users.services.storage import storage_service
from app.modules.auth.models import RefreshToken
from app.shared.security import verify_password, get_password_hash
from app.shared.exceptions import AppException
import logging

logger = logging.getLogger("app")

class UserService:
    def get_user_profile(self, db: Session, user_id: uuid.UUID) -> User:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            raise AppException("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return user

    def update_user_profile(self, db: Session, user_id: uuid.UUID, full_name: str) -> User:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            raise AppException("User not found", status_code=status.HTTP_404_NOT_FOUND)

        old_name = user.full_name
        user_in = UserUpdate(full_name=full_name)
        updated_user = user_repository.update(db, user, user_in)

        # Log activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action=UserActivityType.PROFILE_UPDATE,
            metadata_json={"old_name": old_name, "new_name": full_name}
        )
        logger.info(f"User {user_id} updated profile name to {full_name}")
        return updated_user

    def change_password(self, db: Session, user_id: uuid.UUID, data: ChangePasswordRequest) -> None:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            raise AppException("User not found", status_code=status.HTTP_404_NOT_FOUND)

        if not verify_password(data.old_password, user.password_hash):
            raise AppException("Incorrect current password", status_code=status.HTTP_400_BAD_REQUEST)

        # Update password hash
        user.password_hash = get_password_hash(data.new_password)
        db.commit()

        # Revoke all active refresh tokens for the user
        db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
        db.commit()

        # Log activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action=UserActivityType.PASSWORD_CHANGE,
            metadata_json={"ip_address": None} # Can be extended
        )
        logger.info(f"User {user_id} changed password; all refresh tokens revoked.")

    async def upload_avatar(self, db: Session, user_id: uuid.UUID, file: UploadFile) -> User:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            raise AppException("User not found", status_code=status.HTTP_404_NOT_FOUND)

        # Upload and compress avatar
        avatar_url = await storage_service.upload_avatar(user_id, file)

        # Update user avatar_url
        user_in = UserUpdate(avatar_url=avatar_url)
        user_repository.update(db, user, user_in)

        # Log activity
        user_activity_repository.log_activity(
            db,
            user_id=user_id,
            action=UserActivityType.AVATAR_CHANGE,
            metadata_json={"avatar_url": avatar_url}
        )
        logger.info(f"User {user_id} changed avatar to {avatar_url}")
        return user

    def get_settings(self, db: Session, user_id: uuid.UUID) -> UserSetting:
        settings = user_setting_repository.get_by_user_id(db, user_id)
        if not settings:
            settings = user_setting_repository.create_default(db, user_id)
        return settings

    def update_settings(self, db: Session, user_id: uuid.UUID, settings_in: UserSettingUpdate) -> UserSetting:
        settings = self.get_settings(db, user_id)
        return user_setting_repository.update(db, settings, settings_in)

    def get_activities(self, db: Session, user_id: uuid.UUID, limit: int = 100, offset: int = 0) -> List[UserActivity]:
        return user_activity_repository.get_by_user_id(db, user_id, limit=limit, offset=offset)

user_service = UserService()
