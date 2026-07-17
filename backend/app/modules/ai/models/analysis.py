import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Integer, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class AIAnalysisStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AIRecommendation(str, enum.Enum):
    STRONG_SUBSCRIBE = "Strong Subscribe"
    SUBSCRIBE = "Subscribe"
    NEUTRAL = "Neutral"
    AVOID = "Avoid"

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ipo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ipos.id", ondelete="CASCADE"), index=True, nullable=False)
    
    # Version history support
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # Analysis fields
    status: Mapped[AIAnalysisStatus] = mapped_column(String(50), default=AIAnalysisStatus.PENDING, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    business_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    financial_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    management_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    valuation_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    industry_analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Structured JSON data
    structured_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    
    # Split Scores
    financial_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    management_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    industry_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    valuation_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    overall_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Recommendation and Confidence
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    confidence_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommendation: Mapped[AIRecommendation] = mapped_column(String(50), default=AIRecommendation.NEUTRAL, nullable=False)
    
    # Sync and change detection
    source_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    
    # AI Metadata
    provider: Mapped[str | None] = mapped_column(String(100), nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    # Caching support
    is_cached: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    cache_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    ipo = relationship("IPO", back_populates="ai_analyses")
