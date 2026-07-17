import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class BillingInterval(str, enum.Enum):
    FREE = "FREE"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    NONE = "NONE"

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price_amount: Mapped[int] = mapped_column(Integer, nullable=False) # in paisa (e.g. 49900 for Rs. 499)
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    billing_interval: Mapped[BillingInterval] = mapped_column(String(50), default=BillingInterval.NONE, nullable=False)
    billing_interval_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    subscriptions = relationship("UserSubscription", back_populates="plan")
    payments = relationship("PaymentTransaction", back_populates="plan")
