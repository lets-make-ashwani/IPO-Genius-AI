import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class NotificationEventType(str, enum.Enum):
    IPO_STATUS_UPDATE = "IPO_STATUS_UPDATE"
    IPO_OPEN = "IPO_OPEN"
    IPO_CLOSE = "IPO_CLOSE"
    IPO_LISTED = "IPO_LISTED"
    AI_ANALYSIS_COMPLETED = "AI_ANALYSIS_COMPLETED"
    AI_ANALYSIS_UPDATED = "AI_ANALYSIS_UPDATED"
    WATCHLIST_ADDED = "WATCHLIST_ADDED"
    WATCHLIST_REMINDER = "WATCHLIST_REMINDER"
    SUBSCRIPTION_UPDATED = "SUBSCRIPTION_UPDATED"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    ADMIN_BROADCAST = "ADMIN_BROADCAST"
    SYSTEM_NOTIFICATION = "SYSTEM_NOTIFICATION"

class NotificationPriority(str, enum.Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class NotificationStatus(str, enum.Enum):
    UNREAD = "UNREAD"
    READ = "READ"
    ARCHIVED = "ARCHIVED"

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    
    # Delivery Channels
    in_app_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    email_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    push_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    telegram_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    whatsapp_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Event Preferences mappings
    event_preferences: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="notification_preferences")

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    event_type: Mapped[NotificationEventType] = mapped_column(String(100), nullable=False)
    priority: Mapped[NotificationPriority] = mapped_column(String(50), default=NotificationPriority.NORMAL, nullable=False)
    status: Mapped[NotificationStatus] = mapped_column(String(50), default=NotificationStatus.UNREAD, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # For backward compatibility
    
    # Metadata JSONB
    context_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    
    # Action Support
    action_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    action_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    # Expiration & Soft Delete
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="notifications")

    __table_args__ = (
        Index("ix_notifications_user_status_created", "user_id", "status", "created_at"),
        Index("ix_notifications_deleted_at", "deleted_at"),
    )
