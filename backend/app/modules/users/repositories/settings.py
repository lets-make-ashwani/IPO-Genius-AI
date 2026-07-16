from sqlalchemy.orm import Session
from typing import Optional
import uuid
from app.modules.users.models.settings import UserSetting
from app.modules.users.schemas.settings import UserSettingUpdate

class UserSettingRepository:
    def get_by_user_id(self, db: Session, user_id: uuid.UUID) -> Optional[UserSetting]:
        return db.query(UserSetting).filter(UserSetting.user_id == user_id).first()

    def create_default(self, db: Session, user_id: uuid.UUID) -> UserSetting:
        db_setting = UserSetting(
            id=uuid.uuid4(),
            user_id=user_id,
            theme="light",
            language="en",
            timezone="UTC",
            currency="USD",
            email_notifications=True,
            push_notifications=True,
            marketing_emails=False,
            date_format="YYYY-MM-DD",
            time_format="24h",
            first_day_of_week=1
        )
        db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
        return db_setting

    def update(self, db: Session, settings: UserSetting, settings_in: UserSettingUpdate) -> UserSetting:
        update_data = settings_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(settings, field, value)
        db.commit()
        db.refresh(settings)
        return settings

user_setting_repository = UserSettingRepository()
