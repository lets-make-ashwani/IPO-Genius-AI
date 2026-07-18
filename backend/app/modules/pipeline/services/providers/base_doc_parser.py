from abc import ABC, abstractmethod
from typing import Dict, Any, TypedDict

class ParsedDocumentContent(TypedDict):
    raw_text: str
    extracted_fields: Dict[str, Any]
    document_version: str
    document_hash: str
    document_size: int
    mime_type: str

class BaseDocumentParser(ABC):
    @abstractmethod
    def parse_document(self, url: str, document_type: str) -> ParsedDocumentContent:
        """Downloads, hashes, measures size, and parses a document (DRHP/RHP/Prospectus)."""
        pass
