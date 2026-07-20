import pytest
import asyncio
from app.modules.pipeline.scrapers.nse import NSEScraper
from app.modules.pipeline.scrapers.bse import BSEScraper
from app.modules.pipeline.scrapers.sebi import SEBIScraper
from app.modules.pipeline.scrapers.investorgain import InvestorGainScraper
from app.modules.pipeline.scrapers.chittorgarh import ChittorgarhScraper
from app.modules.pipeline.scrapers.parser import PyMuPDFParser
from app.modules.pipeline.services.providers.gemini_provider import GeminiAIProvider

def test_nse_scraper_discovery():
    scraper = NSEScraper()
    records = asyncio.run(scraper.discover_ipos())
    assert len(records) > 0
    assert records[0]["exchange"] == "NSE"
    assert "company_name" in records[0]

def test_bse_scraper_discovery():
    scraper = BSEScraper()
    records = asyncio.run(scraper.discover_ipos())
    assert len(records) > 0
    assert records[0]["exchange"] == "BSE"

def test_sebi_scraper_discovery():
    scraper = SEBIScraper()
    records = asyncio.run(scraper.discover_ipos())
    assert len(records) > 0

def test_investorgain_scraper_gmp():
    scraper = InvestorGainScraper()
    records = asyncio.run(scraper.discover_ipos())
    assert len(records) > 0
    assert "gmp" in records[0]

def test_chittorgarh_scraper_subscription():
    scraper = ChittorgarhScraper()
    records = asyncio.run(scraper.discover_ipos())
    assert len(records) > 0
    assert "qib_subscription" in records[0]

def test_document_parser():
    parser = PyMuPDFParser()
    result = parser.parse_financial_tables("non_existent_file.pdf")
    assert result["text_length"] == 0

def test_gemini_ai_provider():
    provider = GeminiAIProvider()
    res = asyncio.run(provider.generate_ipo_analysis({"company_name": "Test Co", "sector": "Tech"}))
    assert res["provider"] == "GEMINI"
    assert "recommendation" in res
    assert res["overall_score"] > 0
