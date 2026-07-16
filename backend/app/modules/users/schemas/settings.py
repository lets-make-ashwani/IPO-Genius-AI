from pydantic import BaseModel, Field, ConfigDict
import uuid

class UserSettingBase(BaseModel):
    theme: str = Field("light", max_length=50)
    language: str = Field("en", max_length=10)
    timezone: str = Field("UTC", max_length=50)
    currency: str = Field("USD", max_length=10)
    email_notifications: bool = True
    push_notifications: bool = True
    marketing_emails: bool = False
    date_format: str = Field("YYYY-MM-DD", max_length=50)
    time_format: str = Field("24h", max_length=10)
    first_day_of_week: int = Field(1, ge=0, le=7)

class UserSettingUpdate(BaseModel):
    theme: str | None = Field(None, max_length=50)
    language: str | None = Field(None, max_length=10)
    timezone: str | None = Field(None, max_length=50)
    currency: str | None = Field(None, max_length=10)
    email_notifications: bool | None = None
    push_notifications: bool | None = None
    marketing_emails: bool | None = None
    date_format: str | None = Field(None, max_length=50)
    time_format: str | None = Field(None, max_length=10)
    first_day_of_week: int | None = Field(None, ge=0, le=7)

class UserSettingResponse(UserSettingBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
