import re
from datetime import datetime, date
from typing import Dict, Any
from app.modules.ipos.models.ipo import IPOStatus, IPOExchange, IPOType

class Normalizer:
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes types, currencies, dates, enums, and string formatting
        to ensure consistency with backend schemas and db models.
        """
        normalized = {}

        # 1. Identity & basic strings
        normalized["source_identifier"] = str(raw_data.get("source_identifier", "")).strip()
        normalized["company_name"] = str(raw_data.get("company_name", "")).strip()
        normalized["sector"] = self._clean_string(raw_data.get("sector"))
        normalized["industry"] = self._clean_string(raw_data.get("industry"))
        normalized["logo_url"] = self._clean_string(raw_data.get("logo_url"))
        normalized["source_url"] = self._clean_string(raw_data.get("source_url"))

        # 2. URLs
        normalized["drhp_url"] = self._clean_string(raw_data.get("drhp_url"))
        normalized["rhp_url"] = self._clean_string(raw_data.get("rhp_url"))
        normalized["prospectus_url"] = self._clean_string(raw_data.get("prospectus_url"))

        # 3. Numeric fields
        lot_size = raw_data.get("lot_size")
        if lot_size is not None:
            try:
                normalized["lot_size"] = int(str(lot_size).strip())
            except ValueError:
                normalized["lot_size"] = 0
        else:
            normalized["lot_size"] = 0

        gmp = raw_data.get("gmp")
        if gmp is not None:
            try:
                normalized["gmp"] = int(str(gmp).strip())
            except ValueError:
                normalized["gmp"] = None
        else:
            normalized["gmp"] = None

        # 4. Dates
        normalized["open_date"] = self._normalize_date(raw_data.get("open_date"))
        normalized["close_date"] = self._normalize_date(raw_data.get("close_date"))
        normalized["listing_date"] = self._normalize_date(raw_data.get("listing_date"))

        # 5. Enums
        normalized["status"] = self._normalize_status(raw_data.get("status"))
        normalized["exchange"] = self._normalize_exchange(raw_data.get("exchange"))
        normalized["ipo_type"] = self._normalize_ipo_type(raw_data.get("ipo_type"))

        # 6. String cleanup for price band and issue size
        normalized["price_band"] = self._normalize_currency_string(raw_data.get("price_band"))
        normalized["issue_size"] = self._normalize_currency_string(raw_data.get("issue_size"))

        # 7. Details
        normalized["company_overview"] = self._clean_string(raw_data.get("company_overview"))
        normalized["business_model"] = self._clean_string(raw_data.get("business_model"))
        normalized["promoters"] = self._clean_string(raw_data.get("promoters"))
        normalized["objectives"] = self._clean_string(raw_data.get("objectives"))
        normalized["financial_summary"] = self._clean_string(raw_data.get("financial_summary"))

        return normalized

    def _clean_string(self, val: Any) -> str | None:
        if val is None:
            return None
        s = str(val).strip()
        return s if s else None

    def _normalize_date(self, date_val: Any) -> date | None:
        if not date_val:
            return None
        if isinstance(date_val, date):
            return date_val
        if isinstance(date_val, datetime):
            return date_val.date()
        
        # Try parsing string formats
        s = str(date_val).strip()
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%b %d, %Y", "%d %b %Y"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        return None



    def _normalize_status(self, val: Any) -> str:
        if not val:
            return IPOStatus.UPCOMING.value
        s = str(val).strip().lower()
        if "upcoming" in s:
            return IPOStatus.UPCOMING.value
        if "open" in s:
            return IPOStatus.OPEN.value
        if "closed" in s:
            return IPOStatus.CLOSED.value
        if "listed" in s:
            return IPOStatus.LISTED.value
        
        # Exact match fallback
        for st in IPOStatus:
            if st.value.lower() == s:
                return st.value
        return IPOStatus.UPCOMING.value

    def _normalize_exchange(self, val: Any) -> str:
        if not val:
            return IPOExchange.BOTH.value
        s = str(val).strip().upper()
        if "BSE" in s and "NSE" in s:
            return IPOExchange.BOTH.value
        if "BSE" in s:
            return IPOExchange.BSE.value
        if "NSE" in s:
            return IPOExchange.NSE.value
        return IPOExchange.BOTH.value

    def _normalize_ipo_type(self, val: Any) -> str:
        if not val:
            return IPOType.MAINBOARD.value
        s = str(val).strip().upper()
        if "SME" in s:
            return IPOType.SME.value
        return IPOType.MAINBOARD.value

    def _normalize_currency_string(self, val: Any) -> str:
        if not val:
            return ""
        s = str(val).strip()
        # Ensure ₹ symbol prefix and unified spaces
        s = re.sub(r'\s+', ' ', s)
        # E.g. "Rs. 120" or "Rs 120" -> "₹120"
        s = re.sub(r'(?i)^Rs\.?\s*', '₹', s)
        if not s.startswith('₹'):
            s = '₹' + s
        return s
