from abc import ABC, abstractmethod
from typing import List, TypedDict, Any

class IPODiscoveryRecord(TypedDict):
    source_identifier: str
    company_name: str
    price_band: str
    lot_size: int
    issue_size: str
    open_date: str  # ISO YYYY-MM-DD
    close_date: str # ISO YYYY-MM-DD
    listing_date: str | None # ISO YYYY-MM-DD
    status: str      # E.g. "Upcoming", "Open", "Closed", "Listed"
    exchange: str    # BSE, NSE, BSE & NSE
    ipo_type: str    # MAINBOARD, SME
    sector: str | None
    industry: str | None
    drhp_url: str | None
    rhp_url: str | None
    prospectus_url: str | None
    source_url: str | None
    gmp: int | None
    company_overview: str | None
    business_model: str | None
    promoters: str | None
    objectives: str | None
    financial_summary: str | None

class BaseIPODataProvider(ABC):
    @abstractmethod
    def get_provider_name(self) -> str:
        pass

    @abstractmethod
    def discover_ipos(self) -> List[IPODiscoveryRecord]:
        """Returns all IPO records currently available from this source."""
        pass
