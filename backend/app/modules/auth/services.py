from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional
import uuid
import logging
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate
from app.modules.users.repositories import user_repository
from app.modules.users.models.activity import UserActivityType
from app.modules.users.repositories.activity import user_activity_repository
from app.modules.auth.models import RefreshToken
from app.shared.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    create_password_reset_token,
    decode_password_reset_token
)
from app.shared.exceptions import AppException
from app.shared.email_provider import email_provider
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

    def request_password_reset(self, db: Session, email: str) -> None:
        """
        Initiates a password reset request.
        Generates a stateless JWT token and sends a reset link to the email.
        Always returns success status (to prevent user enumeration).
        """
        user = user_repository.get_by_email(db, email)
        if not user or not user.is_active:
            logger.info(f"Password reset requested for non-existent or inactive email: {email}")
            return

        token = create_password_reset_token(user.email)
        reset_link = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={token}"

        subject = "Reset Your Password - IPO Genius AI"
        body_text = f"Hello {user.full_name},\n\nYou requested a password reset. Please use the following link to reset your password:\n{reset_link}\n\nThis link will expire in 15 minutes.\n\nIf you did not request this, please ignore this email."
        body_html = f"<p>Hello {user.full_name},</p><p>You requested a password reset. Please use the link below to reset your password:</p><p><a href='{reset_link}'>{reset_link}</a></p><p>This link will expire in 15 minutes.</p><p>If you did not request this, please ignore this email.</p>"

        # Send the email using the configured provider
        email_provider.send_email(user.email, subject, body_text, body_html)
        
        # Log activity
        user_activity_repository.log_activity(
            db, 
            user.id, 
            UserActivityType.PASSWORD_RESET_REQUESTED,
            {"email": user.email}
        )

    def reset_password(self, db: Session, token: str, new_password: str) -> None:
        """
        Validates the password reset token and updates the user's password.
        Revokes all active refresh tokens for security.
        """
        email = decode_password_reset_token(token)
        if not email:
            raise AppException("Invalid or expired password reset link", status_code=status.HTTP_400_BAD_REQUEST)

        user = user_repository.get_by_email(db, email)
        if not user or not user.is_active:
            raise AppException("Invalid or expired password reset link", status_code=status.HTTP_400_BAD_REQUEST)

        # Enforce same password rules (length check here, further validation at schema level)
        if len(new_password) < 6:
            raise AppException("Password must be at least 6 characters", status_code=status.HTTP_400_BAD_REQUEST)

        # Update password
        user.password_hash = get_password_hash(new_password)
        db.add(user)

        # Revoke all active refresh tokens immediately
        db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()

        # Log activity
        user_activity_repository.log_activity(
            db,
            user.id,
            UserActivityType.PASSWORD_RESET_COMPLETED
        )
        
        db.commit()

auth_service = AuthService()

