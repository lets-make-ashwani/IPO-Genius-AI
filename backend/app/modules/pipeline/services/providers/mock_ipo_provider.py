from typing import List
from app.modules.pipeline.services.providers.base_ipo_provider import BaseIPODataProvider, IPODiscoveryRecord

class MockIPODataProvider(BaseIPODataProvider):
    def get_provider_name(self) -> str:
        return "MOCK"

    def discover_ipos(self) -> List[IPODiscoveryRecord]:
        return [
            {
                "source_identifier": "mock-techcorp-2026",
                "company_name": "Mock TechCorp India Ltd",
                "price_band": "₹120 - ₹130",
                "lot_size": 100,
                "issue_size": "₹500 Cr",
                "open_date": "2026-08-01",
                "close_date": "2026-08-03",
                "listing_date": "2026-08-08",
                "status": "Upcoming",
                "exchange": "BSE & NSE",
                "ipo_type": "MAINBOARD",
                "sector": "Technology",
                "industry": "SaaS",
                "drhp_url": "https://mock-source.example.com/docs/techcorp-drhp.pdf",
                "rhp_url": "https://mock-source.example.com/docs/techcorp-rhp.pdf",
                "prospectus_url": None,
                "source_url": "https://mock-source.example.com/techcorp",
                "gmp": 15,
                "company_overview": "Mock TechCorp is a leading provider of SaaS enterprise solutions in India.",
                "business_model": "Multi-tenant SaaS subscription models targeting SMBs.",
                "promoters": "Jane Doe, John Smith",
                "objectives": "To fund global marketing campaigns and expand localized hosting regions.",
                "financial_summary": "EBITDA margin of 22% with strong cash flows."
            },
            {
                "source_identifier": "mock-foodie-2026",
                "company_name": "Mock Foodie Nation Ltd",
                "price_band": "₹80 - ₹85",
                "lot_size": 150,
                "issue_size": "₹200 Cr",
                "open_date": "2026-09-10",
                "close_date": "2026-09-12",
                "listing_date": None,
                "status": "Upcoming",
                "exchange": "BSE & NSE",
                "ipo_type": "MAINBOARD",
                "sector": "Consumer Services",
                "industry": "Restaurants",
                "drhp_url": None,
                "rhp_url": None,
                "prospectus_url": None,
                "source_url": "https://mock-source.example.com/foodie",
                "gmp": 5,
                "company_overview": "Mock Foodie operates a chain of quick-service dining restaurants across North India.",
                "business_model": "Franchise-owned company-operated outlet expansion.",
                "promoters": "Alice Cooper, Bob Vance",
                "objectives": "Opening 50 new outlets in Tier 2 cities.",
                "financial_summary": "Net profits increased by 45% year-over-year."
            }
        ]
