from sqlalchemy.orm import Session
from typing import Optional
import uuid
from datetime import datetime, timezone
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserUpdate
from app.shared.security import get_password_hash

class UserRepository:
    def get_by_id(self, db: Session, user_id: uuid.UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user_in: UserCreate) -> User:
        db_user = User(
            id=uuid.uuid4(),
            full_name=user_in.full_name,
            email=user_in.email,
            password_hash=get_password_hash(user_in.password),
            avatar=user_in.avatar,
            role="USER",
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(db_user)
        db.commit()

        db.refresh(db_user)
        return db_user

    def update(self, db: Session, user: User, user_in: UserUpdate) -> User:
        if user_in.full_name is not None:
            user.full_name = user_in.full_name
        if user_in.avatar is not None:
            user.avatar = user_in.avatar
        if user_in.role is not None:
            user.role = user_in.role
        
        db.commit()
        db.refresh(user)
        return user

user_repository = UserRepository()
