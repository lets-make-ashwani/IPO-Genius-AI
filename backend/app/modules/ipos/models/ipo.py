import enum
import uuid
from datetime import datetime, date, timezone
from sqlalchemy import String, Boolean, DateTime, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class IPOStatus(str, enum.Enum):
    UPCOMING = "Upcoming"
    OPEN = "Open"
    CLOSED = "Closed"
    LISTED = "Listed"

class IPOExchange(str, enum.Enum):
    BSE = "BSE"
    NSE = "NSE"
    BOTH = "BSE & NSE"

class IPOType(str, enum.Enum):
    MAINBOARD = "MAINBOARD"
    SME = "SME"

class IPO(Base):
    __tablename__ = "ipos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sector: Mapped[str | None] = mapped_column(String(255), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(255), nullable=True)
    exchange: Mapped[IPOExchange] = mapped_column(String(50), default=IPOExchange.BOTH, nullable=False)
    ipo_type: Mapped[IPOType] = mapped_column(String(50), default=IPOType.MAINBOARD, nullable=False)
    price_band: Mapped[str] = mapped_column(String(100), nullable=False)
    lot_size: Mapped[int] = mapped_column(Integer, nullable=False)
    issue_size: Mapped[str] = mapped_column(String(100), nullable=False)
    open_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    close_date: Mapped[date] = mapped_column(Date, nullable=False)
    listing_date: Mapped[date | None] = mapped_column(Date, index=True, nullable=True)
    status: Mapped[IPOStatus] = mapped_column(String(50), index=True, nullable=False)
    
    # Placeholders for future GMP / Documents
    gmp: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gmp_last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    drhp_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    rhp_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    prospectus_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Scraper & Sync Fields
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    details = relationship("IPODetail", back_populates="ipo", uselist=False, cascade="all, delete-orphan")
