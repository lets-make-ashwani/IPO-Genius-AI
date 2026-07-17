from pydantic import BaseModel, ConfigDict
import uuid
import datetime
from typing import Any, Dict
from app.modules.ai.models.analysis import AIAnalysisStatus, AIRecommendation

class AIAnalysisResponse(BaseModel):
    id: uuid.UUID
    ipo_id: uuid.UUID
    is_active: bool
    version: int
    status: AIAnalysisStatus
    summary: str | None = None
    business_analysis: str | None = None
    financial_analysis: str | None = None
    risk_analysis: str | None = None
    management_analysis: str | None = None
    valuation_analysis: str | None = None
    industry_analysis: str | None = None
    
    # Structured JSON data
    structured_data: Dict[str, Any] | None = None
    
    # Split Scores
    financial_score: int
    management_score: int
    industry_score: int
    risk_score: int
    valuation_score: int
    overall_score: int
    
    # Recommendation and Confidence
    confidence_score: float
    confidence_reason: str | None = None
    recommendation: AIRecommendation
    
    # Sync and change detection
    source_hash: str | None = None
    
    # AI Metadata
    provider: str | None = None
    model_name: str | None = None
    prompt_version: str | None = None
    tokens_used: int | None = None
    processing_time_ms: int | None = None
    
    # Caching support
    is_cached: bool
    cache_expires_at: datetime.datetime | None = None
    
    generated_at: datetime.datetime
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class AISummaryResponse(BaseModel):
    summary: str | None = None
    status: AIAnalysisStatus
    recommendation: AIRecommendation
    overall_score: int
    is_cached: bool
    generated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class AIScoreResponse(BaseModel):
    financial_score: int
    management_score: int
    industry_score: int
    risk_score: int
    valuation_score: int
    overall_score: int
    confidence_score: float
    confidence_reason: str | None = None
    recommendation: AIRecommendation
    generated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class AIRiskResponse(BaseModel):
    risk_analysis: str | None = None
    risk_score: int
    status: AIAnalysisStatus
    generated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
