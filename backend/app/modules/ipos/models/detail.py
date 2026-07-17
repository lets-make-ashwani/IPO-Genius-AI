import uuid
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class IPODetail(Base):
    __tablename__ = "ipo_details"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ipo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ipos.id", ondelete="CASCADE"), unique=True, nullable=False)
    company_overview: Mapped[str | None] = mapped_column(Text, nullable=True)
    business_model: Mapped[str | None] = mapped_column(Text, nullable=True)
    promoters: Mapped[str | None] = mapped_column(Text, nullable=True)
    objectives: Mapped[str | None] = mapped_column(Text, nullable=True)
    financial_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    ipo = relationship("IPO", back_populates="details")
