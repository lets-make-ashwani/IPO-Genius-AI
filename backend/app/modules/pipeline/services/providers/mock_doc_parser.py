import hashlib
from app.modules.pipeline.services.providers.base_doc_parser import BaseDocumentParser, ParsedDocumentContent

class MockDocumentParser(BaseDocumentParser):
    def parse_document(self, url: str, document_type: str) -> ParsedDocumentContent:
        content_str = f"Mock text content for document at {url} ({document_type})"
        doc_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
        
        return {
            "raw_text": content_str,
            "extracted_fields": {
                "financial_metrics_extracted": "EBITDA 22%, PAT 18Cr",
                "promoters_list": ["Jane Doe", "John Smith"],
                "company_details": "Mock TechCorp India Ltd"
            },
            "document_version": "1.0.0",
            "document_hash": doc_hash,
            "document_size": len(content_str),
            "mime_type": "application/pdf"
        }
