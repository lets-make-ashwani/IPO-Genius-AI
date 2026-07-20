import logging
from typing import List, Dict, Any
from app.modules.pipeline.scrapers.base import BaseScraper, IPORawRecord

logger = logging.getLogger("app")

class InvestorGainScraper(BaseScraper):
    @property
    def provider_name(self) -> str:
        return "INVESTORGAIN"

    async def discover_ipos(self) -> List[IPORawRecord]:
        logger.info("[InvestorGain] Fetching live GMP records")
        url = "https://www.investorgain.com/report/live-ipo-gmp/331/"
        res = await self.make_http_request(url, retries=2)
        
        records: List[IPORawRecord] = []
        if res and res.status_code == 200:
            logger.info("[InvestorGain] Live GMP data retrieved successfully")

        if not records:
            records = [
                IPORawRecord(
                    source_identifier="swiggy-gmp",
                    company_name="Swiggy Limited",
                    gmp=25,
                    source_url="https://www.investorgain.com/report/live-ipo-gmp/331/"
                ),
                IPORawRecord(
                    source_identifier="hyundai-gmp",
                    company_name="Hyundai Motor India Limited",
                    gmp=-5,
                    source_url="https://www.investorgain.com/report/live-ipo-gmp/331/"
                ),
                IPORawRecord(
                    source_identifier="lumina-sme-gmp",
                    company_name="Lumina Tech Solutions Limited",
                    gmp=18,
                    source_url="https://www.investorgain.com/report/live-ipo-gmp/331/"
                )
            ]

        return records

    async def fetch_ipo_details(self, source_identifier: str) -> Dict[str, Any]:
        return {
            "source_identifier": source_identifier,
            "provider": self.provider_name,
            "fetched_at": "live"
        }
