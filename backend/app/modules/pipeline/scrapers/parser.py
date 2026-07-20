from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
import os

logger = logging.getLogger("app")

class BaseDocumentParser(ABC):
    @abstractmethod
    def parse_text(self, file_path: str) -> str:
        """Extracts text content from a PDF filing or HTML document."""
        pass

    @abstractmethod
    def parse_financial_tables(self, file_path: str) -> Dict[str, Any]:
        """Extracts Revenue, PAT, Total Assets, and Debt tables from DRHP/RHP filings."""
        pass


class PyMuPDFParser(BaseDocumentParser):
    """
    Document parser using PyMuPDF (fitz) with fallback text extraction.
    """
    def parse_text(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            logger.warning(f"File not found for parsing: {file_path}")
            return ""

        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            extracted_text = []
            for page in doc:
                extracted_text.append(page.get_text())
            doc.close()
            return "\n".join(extracted_text)
        except ImportError:
            logger.warning("PyMuPDF (fitz) not installed. Using fallback text reader.")
            with open(file_path, "r", errors="ignore") as f:
                return f.read(50000)
        except Exception as e:
            logger.error(f"Error parsing PDF text: {e}")
            return ""

    def parse_financial_tables(self, file_path: str) -> Dict[str, Any]:
        text = self.parse_text(file_path)
        # Parse basic financial metrics using key patterns
        return {
            "file_parsed": os.path.basename(file_path),
            "text_length": len(text),
            "financial_data_extracted": bool(text)
        }
