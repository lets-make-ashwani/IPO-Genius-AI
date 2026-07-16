from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid
from typing import Dict, Any, Optional

class UserActivityResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    action: str
    metadata: Optional[Dict[str, Any]] = Field(default=None, validation_alias="metadata_json")
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
