from abc import ABC, abstractmethod
from typing import List, TypedDict, Optional, Dict, Any
import httpx
import logging
import asyncio
import random

logger = logging.getLogger("app")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

class IPORawRecord(TypedDict, total=False):
    source_identifier: str
    company_name: str
    price_band: Optional[str]
    lot_size: Optional[int]
    issue_size: Optional[str]
    open_date: Optional[str]
    close_date: Optional[str]
    listing_date: Optional[str]
    status: Optional[str]
    exchange: Optional[str]
    ipo_type: Optional[str]
    sector: Optional[str]
    industry: Optional[str]
    drhp_url: Optional[str]
    rhp_url: Optional[str]
    prospectus_url: Optional[str]
    source_url: Optional[str]
    gmp: Optional[int]
    qib_subscription: Optional[float]
    nii_subscription: Optional[float]
    retail_subscription: Optional[float]
    total_subscription: Optional[float]
    company_overview: Optional[str]
    business_model: Optional[str]
    promoters: Optional[str]
    objectives: Optional[str]
    financial_summary: Optional[Dict[str, Any]]

class BaseScraper(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique name identifier of the scraper provider."""
        pass

    @abstractmethod
    async def discover_ipos(self) -> List[IPORawRecord]:
        """Discovers recent, upcoming, open, and closed IPO listings from this source."""
        pass

    @abstractmethod
    async def fetch_ipo_details(self, source_identifier: str) -> Dict[str, Any]:
        """Fetches detailed metrics, subscription data, or documents for an IPO."""
        pass

    def get_headers(self) -> Dict[str, str]:
        """Generates polite headers with user-agent rotation."""
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Connection": "keep-alive"
        }

    async def make_http_request(
        self, 
        url: str, 
        method: str = "GET", 
        json_data: Optional[Dict[str, Any]] = None,
        retries: int = 3,
        delay: float = 1.5
    ) -> Optional[httpx.Response]:
        """Executes an HTTP request with exponential backoff retries and polite delays."""
        for attempt in range(1, retries + 1):
            try:
                await asyncio.sleep(delay * attempt)
                async with httpx.AsyncClient(headers=self.get_headers(), timeout=30.0, follow_redirects=True) as client:
                    if method.upper() == "POST":
                        res = await client.post(url, json=json_data)
                    else:
                        res = await client.get(url)
                    
                    if res.status_code == 200:
                        return res
                    else:
                        logger.warning(f"[{self.provider_name}] HTTP {res.status_code} on attempt {attempt} for URL: {url}")
            except Exception as e:
                logger.error(f"[{self.provider_name}] Request error on attempt {attempt} for URL {url}: {e}")
            
        return None
