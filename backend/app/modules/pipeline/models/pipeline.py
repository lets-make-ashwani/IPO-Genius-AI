import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer, Float, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class PipelineRunStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    WAITING = "WAITING"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class PipelineRunTrigger(str, enum.Enum):
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"
    WEBHOOK = "WEBHOOK"

class PipelineItemStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    WAITING = "WAITING"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"
    FAILED = "FAILED"

class PipelineItemStage(str, enum.Enum):
    DISCOVERY = "DISCOVERY"
    DOCUMENT_FETCH = "DOCUMENT_FETCH"
    EXTRACTION = "EXTRACTION"
    NORMALIZATION = "NORMALIZATION"
    VALIDATION = "VALIDATION"
    IPO_UPSERT = "IPO_UPSERT"
    AI_GENERATION = "AI_GENERATION"
    NOTIFICATION = "NOTIFICATION"
    COMPLETED = "COMPLETED"

class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    idempotency_key: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    status: Mapped[PipelineRunStatus] = mapped_column(String(50), default=PipelineRunStatus.PENDING, index=True, nullable=False)
    trigger: Mapped[PipelineRunTrigger] = mapped_column(String(50), default=PipelineRunTrigger.MANUAL, nullable=False)
    source_provider: Mapped[str] = mapped_column(String(100), nullable=False)
    triggered_by_admin_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    total_discovered: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_processed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_skipped: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_failed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    run_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    items = relationship("PipelineRunItem", back_populates="run", cascade="all, delete-orphan")
    triggered_by = relationship("User")

class PipelineRunItem(Base):
    __tablename__ = "pipeline_run_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pipeline_runs.id", ondelete="CASCADE"), index=True, nullable=False)

    source_identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[PipelineItemStatus] = mapped_column(String(50), default=PipelineItemStatus.PENDING, index=True, nullable=False)
    current_stage: Mapped[PipelineItemStage] = mapped_column(String(50), default=PipelineItemStage.DISCOVERY, nullable=False)

    ipo_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("ipos.id", ondelete="SET NULL"), nullable=True)
    source_data_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    extracted_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    normalized_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    validation_errors: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # AI execution metrics
    ai_provider: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ai_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ai_tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ai_processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ai_estimated_cost: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    run = relationship("PipelineRun", back_populates="items")
    ipo = relationship("IPO")

class IPODocument(Base):
    __tablename__ = "ipo_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ipo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ipos.id", ondelete="CASCADE"), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False) # e.g. "DRHP", "RHP", "PROSPECTUS"
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    document_version: Mapped[str] = mapped_column(String(50), nullable=False)
    document_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    document_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    ipo = relationship("IPO")
