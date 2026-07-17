from pydantic import BaseModel, ConfigDict, Field, field_validator
import uuid
import datetime
from typing import Optional, List, Dict, Any

class AdminUserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class SignupStats(BaseModel):
    date: str
    count: int

class ActivityLogEntry(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    action: str
    metadata_json: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class DashboardData(BaseModel):
    total_users: int
    total_ipos: int
    total_watchlist_items: int
    total_ai_analyses: int
    recent_signups: List[SignupStats]
    recent_activities: List[ActivityLogEntry]

class AdminDashboardResponse(BaseModel):
    success: bool
    message: str
    data: DashboardData

class AdminUserUpdatePayload(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("role")
    def validate_role(cls, v):
        if v is not None and v not in ["USER", "ADMIN"]:
            raise ValueError("Role must be either USER or ADMIN")
        return v
