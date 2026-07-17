import enum
import uuid
import sqlalchemy as sa
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Integer, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class PaymentStatus(str, enum.Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class PaymentTransaction(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subscription_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True)
    plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("subscription_plans.id"), nullable=False)
    
    # Immutability snapshots
    plan_code: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False) # snapshotted amount in paisa
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)

    status: Mapped[PaymentStatus] = mapped_column(String(50), default=PaymentStatus.CREATED, index=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(50), default="MOCK", nullable=False)
    provider_order_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    provider_payment_id: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    provider_signature: Mapped[str | None] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    idempotency_key: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    user = relationship("User", back_populates="payments")
    subscription = relationship("UserSubscription", back_populates="payments")
    plan = relationship("SubscriptionPlan", back_populates="payments")

# Double protection composite indexes for performance
Index("ix_payments_user_created_at", "user_id", "created_at")
Index("ix_payments_status_created_at", "status", "created_at")
