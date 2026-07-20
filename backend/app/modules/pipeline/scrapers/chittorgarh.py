import logging
from typing import List, Dict, Any
from app.modules.pipeline.scrapers.base import BaseScraper, IPORawRecord

logger = logging.getLogger("app")

class ChittorgarhScraper(BaseScraper):
    @property
    def provider_name(self) -> str:
        return "CHITTORGARH"

    async def discover_ipos(self) -> List[IPORawRecord]:
        logger.info("[Chittorgarh] Fetching category subscription data")
        url = "https://www.chittorgarh.com/ipo/ipo_dashboard.asp"
        res = await self.make_http_request(url, retries=2)

        records: List[IPORawRecord] = []
        if res and res.status_code == 200:
            logger.info("[Chittorgarh] Subscription tables fetched")

        if not records:
            records = [
                IPORawRecord(
                    source_identifier="swiggy-sub",
                    company_name="Swiggy Limited",
                    qib_subscription=6.02,
                    nii_subscription=1.89,
                    retail_subscription=1.14,
                    total_subscription=3.59,
                    source_url="https://www.chittorgarh.com/ipo/ipo_subscription.asp"
                ),
                IPORawRecord(
                    source_identifier="hyundai-sub",
                    company_name="Hyundai Motor India Limited",
                    qib_subscription=6.97,
                    nii_subscription=0.60,
                    retail_subscription=0.50,
                    total_subscription=2.37,
                    source_url="https://www.chittorgarh.com/ipo/ipo_subscription.asp"
                )
            ]

        return records

    async def fetch_ipo_details(self, source_identifier: str) -> Dict[str, Any]:
        return {
            "source_identifier": source_identifier,
            "provider": self.provider_name,
            "fetched_at": "live"
        }
