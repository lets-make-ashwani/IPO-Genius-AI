from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timezone
from app.modules.users.models.activity import UserActivity, UserActivityType

class UserActivityRepository:
    def log_activity(
        self,
        db: Session,
        user_id: uuid.UUID,
        action: UserActivityType,
        metadata_json: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        db_activity = UserActivity(
            id=uuid.uuid4(),
            user_id=user_id,
            action=action.value,
            metadata_json=metadata_json,
            created_at=datetime.now(timezone.utc)
        )
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity

    def get_by_user_id(
        self,
        db: Session,
        user_id: uuid.UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[UserActivity]:
        return (
            db.query(UserActivity)
            .filter(UserActivity.user_id == user_id)
            .order_by(desc(UserActivity.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )

user_activity_repository = UserActivityRepository()
