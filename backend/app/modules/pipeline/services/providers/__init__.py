from typing import Any
from app.modules.pipeline.services.providers.base_ipo_provider import BaseIPODataProvider, IPODiscoveryRecord
from app.modules.pipeline.services.providers.mock_ipo_provider import MockIPODataProvider
from app.modules.pipeline.services.providers.base_doc_parser import BaseDocumentParser, ParsedDocumentContent
from app.modules.pipeline.services.providers.mock_doc_parser import MockDocumentParser
from app.modules.pipeline.scrapers.base import BaseScraper
from app.modules.pipeline.scrapers.nse import NSEScraper
from app.modules.pipeline.scrapers.bse import BSEScraper
from app.modules.pipeline.scrapers.sebi import SEBIScraper
from app.modules.pipeline.scrapers.investorgain import InvestorGainScraper
from app.modules.pipeline.scrapers.chittorgarh import ChittorgarhScraper
from app.modules.pipeline.scrapers.parser import PyMuPDFParser

def get_ipo_data_provider(provider_name: str) -> Any:
    p = provider_name.upper()
    if p == "NSE":
        return NSEScraper()
    elif p == "BSE":
        return BSEScraper()
    elif p == "SEBI":
        return SEBIScraper()
    elif p == "INVESTORGAIN":
        return InvestorGainScraper()
    elif p == "CHITTORGARH":
        return ChittorgarhScraper()
    elif p == "MOCK":
        return MockIPODataProvider()
    else:
        # Fallback default provider
        return NSEScraper()

def get_document_parser(parser_name: str = "PYMUPDF") -> Any:
    if parser_name.upper() in ("PYMUPDF", "DEFAULT"):
        return PyMuPDFParser()
    return MockDocumentParser()
