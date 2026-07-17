from pydantic import BaseModel, ConfigDict
import uuid
import datetime
from typing import Optional, Dict, List
from app.modules.notifications.models.notification import NotificationEventType, NotificationPriority, NotificationStatus


class NotificationResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    message: str
    event_type: NotificationEventType
    priority: NotificationPriority
    status: NotificationStatus
    is_read: bool
    context_metadata: Optional[Dict] = None
    action_label: Optional[str] = None
    action_url: Optional[str] = None
    expires_at: Optional[datetime.datetime] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationPreferenceResponse(BaseModel):
    in_app_enabled: bool
    email_enabled: bool
    push_enabled: bool
    telegram_enabled: bool
    whatsapp_enabled: bool
    event_preferences: Dict

    model_config = ConfigDict(from_attributes=True)

class NotificationPreferenceUpdate(BaseModel):
    in_app_enabled: Optional[bool] = None
    email_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    telegram_enabled: Optional[bool] = None
    whatsapp_enabled: Optional[bool] = None
    event_preferences: Optional[Dict] = None

