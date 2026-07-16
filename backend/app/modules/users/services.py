from sqlalchemy.orm import Session
from typing import Optional
import uuid
from app.modules.users.models import User
from app.modules.users.schemas import UserUpdate
from app.modules.users.repositories import user_repository
from app.shared.exceptions import AppException
from fastapi import status

class UserService:
    def get_user_profile(self, db: Session, user_id: uuid.UUID) -> User:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            raise AppException("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return user

    def update_user_profile(self, db: Session, user_id: uuid.UUID, user_in: UserUpdate) -> User:
        user = user_repository.get_by_id(db, user_id)
        if not user:
            raise AppException("User not found", status_code=status.HTTP_404_NOT_FOUND)
        return user_repository.update(db, user, user_in)

user_service = UserService()
