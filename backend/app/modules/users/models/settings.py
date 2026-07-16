import uuid
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class UserSetting(Base):
    __tablename__ = "settings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    theme: Mapped[str] = mapped_column(String(50), default="light", nullable=False)
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    email_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    push_notifications: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    marketing_emails: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    date_format: Mapped[str] = mapped_column(String(50), default="YYYY-MM-DD", nullable=False)
    time_format: Mapped[str] = mapped_column(String(10), default="24h", nullable=False)
    first_day_of_week: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relationships
    user = relationship("User", back_populates="settings")
