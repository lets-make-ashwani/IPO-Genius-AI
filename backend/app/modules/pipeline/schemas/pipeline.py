from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from app.modules.pipeline.models.pipeline import PipelineRunStatus, PipelineRunTrigger, PipelineItemStatus, PipelineItemStage

class PipelineTriggerRequest(BaseModel):
    provider: str = "MOCK"
    idempotency_key: Optional[str] = None
    force_reprocess: bool = False

class PipelineRunSummaryResponse(BaseModel):
    id: uuid.UUID
    idempotency_key: str
    status: PipelineRunStatus
    trigger: PipelineRunTrigger
    source_provider: str
    triggered_by_admin_id: Optional[uuid.UUID]
    total_discovered: int
    total_processed: int
    total_skipped: int
    total_failed: int
    started_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)

class PipelineRunItemResponse(BaseModel):
    id: uuid.UUID
    run_id: uuid.UUID
    source_identifier: str
    company_name: str
    status: PipelineItemStatus
    current_stage: PipelineItemStage
    ipo_id: Optional[uuid.UUID]
    source_data_hash: Optional[str]
    error_message: Optional[str]
    retry_count: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    extracted_data: Optional[Dict[str, Any]]
    normalized_data: Optional[Dict[str, Any]]
    validation_errors: Optional[Dict[str, Any]]
    ai_provider: Optional[str]
    ai_model: Optional[str]
    ai_tokens_used: Optional[int]
    ai_processing_time_ms: Optional[int]
    ai_estimated_cost: Optional[float]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PipelineRunResponse(PipelineRunSummaryResponse):
    items: List[PipelineRunItemResponse] = []

    model_config = ConfigDict(from_attributes=True)

class PipelineRunListResponse(BaseModel):
    items: List[PipelineRunSummaryResponse]
    total: int
    limit: int
    offset: int
