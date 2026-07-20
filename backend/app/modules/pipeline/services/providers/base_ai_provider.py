from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    async def generate_ipo_analysis(self, ipo_data: Dict[str, Any], document_text: str = "") -> Dict[str, Any]:
        """Generates structured SWOT analysis, scores, and investment recommendation."""
        pass
