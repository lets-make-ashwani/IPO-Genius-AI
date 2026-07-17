from pydantic import BaseModel, ConfigDict
import uuid
import datetime
from app.modules.ipos.models.ipo import IPOStatus, IPOExchange, IPOType

class IPODetailResponse(BaseModel):
    company_overview: str | None = None
    business_model: str | None = None
    promoters: str | None = None
    objectives: str | None = None
    financial_summary: str | None = None

    model_config = ConfigDict(from_attributes=True)

class IPOResponse(BaseModel):
    id: uuid.UUID
    company_name: str
    slug: str
    logo_url: str | None = None
    sector: str | None = None
    industry: str | None = None
    exchange: IPOExchange
    ipo_type: IPOType
    price_band: str
    lot_size: int
    issue_size: str
    open_date: datetime.date
    close_date: datetime.date
    listing_date: datetime.date | None = None
    status: IPOStatus
    
    # Placeholders for future GMP / Documents
    gmp: int | None = None
    gmp_last_updated: datetime.datetime | None = None
    drhp_url: str | None = None
    rhp_url: str | None = None
    prospectus_url: str | None = None

    # Scraper & Sync Fields
    source: str | None = None
    source_url: str | None = None
    last_synced_at: datetime.datetime | None = None
    is_verified: bool

    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class IPODetailExtendedResponse(IPOResponse):
    details: IPODetailResponse | None = None
