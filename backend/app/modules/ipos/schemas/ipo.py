from pydantic import BaseModel, ConfigDict
import uuid
import datetime
from typing import Optional
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
    total_subscription: Optional[float] = 0.0
    drhp_url: str | None = None
    rhp_url: str | None = None
    prospectus_url: str | None = None

    # Dynamic classification fields computed relative to current date
    computed_status: Optional[str] = None
    listing_today: Optional[bool] = False
    opening_today: Optional[bool] = False
    opening_tomorrow: Optional[bool] = False
    closing_today: Optional[bool] = False
    closing_tomorrow: Optional[bool] = False

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

class IPOAnalysisResponse(BaseModel):
    ipo_id: uuid.UUID
    overall_score: int
    financial_score: int | None = None
    management_score: int | None = None
    valuation_score: int | None = None
    risk_score: int | None = None
    recommendation: str
    summary: str | None = None
    strengths: list[str] = []
    weaknesses: list[str] = []
    risks: list[str] = []
    model_provider: str | None = None
    model_version: str | None = None

class IPOFinancialsResponse(BaseModel):
    ipo_id: uuid.UUID
    financial_summary: str | None = None
    revenue_growth: str | None = "N/A"
    ebitda_margin: str | None = "N/A"
    pat_margin: str | None = "N/A"

class IPOSubscriptionResponse(BaseModel):
    ipo_id: uuid.UUID
    qib_subscription: float = 0.0
    nii_subscription: float = 0.0
    retail_subscription: float = 0.0
    employee_subscription: float = 0.0
    total_subscription: float = 0.0
    last_updated_at: datetime.datetime | None = None

class IPODocumentsResponse(BaseModel):
    ipo_id: uuid.UUID
    drhp_url: str | None = None
    rhp_url: str | None = None
    prospectus_url: str | None = None

class IPONewsItem(BaseModel):
    title: str
    source: str
    url: str
    published_at: str
    sentiment: str = "NEUTRAL"

class IPONewsResponse(BaseModel):
    ipo_id: uuid.UUID
    articles: list[IPONewsItem] = []


class IPODetailCreate(BaseModel):
    company_overview: Optional[str] = None
    business_model: Optional[str] = None
    promoters: Optional[str] = None
    objectives: Optional[str] = None
    financial_summary: Optional[str] = None

class IPOCreate(BaseModel):
    company_name: str
    slug: Optional[str] = None
    logo_url: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    exchange: IPOExchange
    ipo_type: IPOType
    price_band: str
    lot_size: int
    issue_size: str
    open_date: datetime.date
    close_date: datetime.date
    listing_date: Optional[datetime.date] = None
    status: IPOStatus
    gmp: Optional[int] = None
    gmp_last_updated: Optional[datetime.datetime] = None
    total_subscription: Optional[float] = 0.0
    drhp_url: Optional[str] = None
    rhp_url: Optional[str] = None
    prospectus_url: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    is_verified: bool = True
    details: Optional[IPODetailCreate] = None

class IPOUpdate(BaseModel):
    company_name: Optional[str] = None
    slug: Optional[str] = None
    logo_url: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    exchange: Optional[IPOExchange] = None
    ipo_type: Optional[IPOType] = None
    price_band: Optional[str] = None
    lot_size: Optional[int] = None
    issue_size: Optional[str] = None
    open_date: Optional[datetime.date] = None
    close_date: Optional[datetime.date] = None
    listing_date: Optional[datetime.date] = None
    status: Optional[IPOStatus] = None
    gmp: Optional[int] = None
    gmp_last_updated: Optional[datetime.datetime] = None
    total_subscription: Optional[float] = None
    drhp_url: Optional[str] = None
    rhp_url: Optional[str] = None
    prospectus_url: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    is_verified: Optional[bool] = None
    details: Optional[IPODetailCreate] = None

