from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Tuple
import uuid
import logging
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate
from app.modules.users.repositories import user_repository
from app.modules.auth.models import RefreshToken
from app.shared.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.shared.exceptions import AppException
from app.config.settings import settings
from fastapi import status

logger = logging.getLogger("app")

class AuthService:
    def register_user(self, db: Session, register_in: UserCreate) -> User:
        # Check duplicate email
        existing_user = user_repository.get_by_email(db, register_in.email)
        if existing_user:
            raise AppException("Email already registered", status_code=status.HTTP_400_BAD_REQUEST)
        
        return user_repository.create(db, register_in)

    def login_user(self, db: Session, email: str, password: str) -> Tuple[User, str, str]:
        user = user_repository.get_by_email(db, email)
        if not user or not user.is_active:
            raise AppException("Invalid email or password", status_code=status.HTTP_401_UNAUTHORIZED)

        if not verify_password(password, user.password_hash):
            raise AppException("Invalid email or password", status_code=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens
        token_data = {"sub": str(user.id), "email": user.email, "role": user.role}
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        # Save refresh token in database
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        db_token = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=expires_at
        )
        db.add(db_token)
        db.commit()

        return user, access_token, refresh_token

    def refresh_access_token(self, db: Session, refresh_token: str) -> Tuple[User, str, str]:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AppException("Invalid refresh token", status_code=status.HTTP_401_UNAUTHORIZED)

        # Verify from database
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.is_revoked == False
        ).first()

        if not db_token:
            raise AppException("Refresh token revoked or invalid", status_code=status.HTTP_401_UNAUTHORIZED)

        # Check expiration
        # Ensure comparison is timezone aware or naive depending on database setup (Postgres DateTime(timezone=True) is timezone aware in python)
        expires_at = db_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        if expires_at < datetime.now(timezone.utc):
            db.delete(db_token)
            db.commit()
            raise AppException("Refresh token expired", status_code=status.HTTP_401_UNAUTHORIZED)

        # Get user
        user = user_repository.get_by_id(db, db_token.user_id)
        if not user or not user.is_active:
            raise AppException("User inactive or not found", status_code=status.HTTP_401_UNAUTHORIZED)

        # Rotate refresh token (highly secure: delete old, generate new)
        db.delete(db_token)
        
        token_data = {"sub": str(user.id), "email": user.email, "role": user.role}
        new_access_token = create_access_token(data=token_data)
        new_refresh_token = create_refresh_token(data=token_data)

        new_expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        new_db_token = RefreshToken(
            user_id=user.id,
            token=new_refresh_token,
            expires_at=new_expires_at
        )
        db.add(new_db_token)
        db.commit()

        return user, new_access_token, new_refresh_token

    def revoke_refresh_token(self, db: Session, token: str) -> None:
        db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if db_token:
            db.delete(db_token)
            db.commit()

auth_service = AuthService()
