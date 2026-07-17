from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_analysis(self, company_name: str, ipo_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates structured AI analysis for an IPO.
        """
        pass

class MockAIProvider(BaseAIProvider):
    def generate_analysis(self, company_name: str, ipo_details: Dict[str, Any]) -> Dict[str, Any]:
        # Emulate processing delay or computation
        return {
            "summary": f"{company_name} is showing solid operational growth in its respective sector.",
            "business_analysis": "The business operates a diversified SaaS model with high recurring revenue.",
            "financial_analysis": "Strong balance sheet, cashflow positive for last 3 years with 25% CAGR.",
            "risk_analysis": "Primary risks include high dependency on third-party cloud infrastructure and regulatory compliance.",
            "management_analysis": "Experienced leadership with average promoter tenure of over 10 years.",
            "valuation_analysis": "P/E ratio of 22x is in line with the industry average of 24x, suggesting fair pricing.",
            "industry_analysis": "The industry is experiencing a tailwind driven by digital transformation adoption.",
            "structured_data": {
                "strengths": ["Recurring revenue model", "Strong balance sheet"],
                "weaknesses": ["Customer concentration risk"]
            },
            "financial_score": 85,
            "management_score": 80,
            "industry_score": 75,
            "risk_score": 70,
            "valuation_score": 72,
            "overall_score": 76,
            "confidence_score": 0.88,
            "confidence_reason": "Based on complete DRHP statements and verified past audited balance sheets.",
            "recommendation": "Subscribe",
            "provider": "MOCK",
            "model_name": "mock-llm-v1",
            "prompt_version": "1.0",
            "tokens_used": 845,
            "processing_time_ms": 250
        }
