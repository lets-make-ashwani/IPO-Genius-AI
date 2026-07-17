from pydantic import BaseModel, ConfigDict
import uuid
import datetime
from typing import List, Optional
from app.modules.watchlist.models.watchlist import WatchlistPriority
from app.modules.ipos.schemas.ipo import IPOResponse

class WatchlistFolderResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    color: str | None = None
    is_default: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class WatchlistItemResponse(BaseModel):
    id: uuid.UUID
    folder_id: uuid.UUID
    ipo_id: uuid.UUID
    notes: str | None = None
    tags: List[str] | None = None
    priority: WatchlistPriority
    reminder_enabled: bool
    reminder_date: datetime.datetime | None = None
    
    # AI Snapshot
    ai_overall_score: int | None = None
    ai_recommendation: str | None = None
    ai_confidence_score: float | None = None
    
    deleted_at: datetime.datetime | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    # Nested IPO Details
    ipo: IPOResponse

    model_config = ConfigDict(from_attributes=True)

class WatchlistItemCreate(BaseModel):
    ipo_id: uuid.UUID
    folder_id: Optional[uuid.UUID] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[WatchlistPriority] = WatchlistPriority.MEDIUM
    reminder_enabled: Optional[bool] = False
    reminder_date: Optional[datetime.datetime] = None

class WatchlistItemUpdate(BaseModel):
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[WatchlistPriority] = None
    reminder_enabled: Optional[bool] = None
    reminder_date: Optional[datetime.datetime] = None

class WatchlistSummaryResponse(BaseModel):
    total_count: int
    upcoming_count: int
    open_count: int
    closed_count: int
    listed_count: int
