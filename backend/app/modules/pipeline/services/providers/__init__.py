from app.modules.pipeline.services.providers.base_ipo_provider import BaseIPODataProvider, IPODiscoveryRecord
from app.modules.pipeline.services.providers.mock_ipo_provider import MockIPODataProvider
from app.modules.pipeline.services.providers.base_doc_parser import BaseDocumentParser, ParsedDocumentContent
from app.modules.pipeline.services.providers.mock_doc_parser import MockDocumentParser

def get_ipo_data_provider(provider_name: str) -> BaseIPODataProvider:
    if provider_name.upper() == "MOCK":
        return MockIPODataProvider()
    raise ValueError(f"Unknown IPO data provider: {provider_name}")

def get_document_parser(parser_name: str = "MOCK") -> BaseDocumentParser:
    if parser_name.upper() == "MOCK":
        return MockDocumentParser()
    raise ValueError(f"Unknown document parser: {parser_name}")
