import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Integer, Float, ForeignKey, Text, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class WatchlistPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class WatchlistFolder(Base):
    __tablename__ = "watchlist_folders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    color: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="watchlist_folders")
    items = relationship("WatchlistItem", back_populates="folder", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_folder_name"),
    )

class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    folder_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("watchlist_folders.id", ondelete="CASCADE"), index=True, nullable=False)
    ipo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ipos.id", ondelete="CASCADE"), index=True, nullable=False)
    
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    priority: Mapped[WatchlistPriority] = mapped_column(String(50), default=WatchlistPriority.MEDIUM, nullable=False)
    
    # Reminders
    reminder_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reminder_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # AI Snapshot
    ai_overall_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ai_recommendation: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ai_confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # Soft delete support
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    folder = relationship("WatchlistFolder", back_populates="items")
    ipo = relationship("IPO", back_populates="watchlist_items")

    __table_args__ = (
        Index("ix_active_folder_ipo", "folder_id", "ipo_id", unique=True, postgresql_where=(deleted_at == None)),
    )
