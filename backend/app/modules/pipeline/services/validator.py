from typing import Dict, Any, List, TypedDict
from datetime import date
from app.modules.ipos.models.ipo import IPOStatus, IPOExchange, IPOType

class ValidationResult(TypedDict):
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class IPODataValidator:
    REQUIRED_FIELDS = [
        "company_name",
        "price_band",
        "lot_size",
        "issue_size",
        "open_date",
        "close_date",
        "status",
        "exchange",
        "ipo_type",
    ]

    def validate(self, record: Dict[str, Any]) -> ValidationResult:
        errors = []
        warnings = []

        # 1. Required field checks
        for field in self.REQUIRED_FIELDS:
            val = record.get(field)
            if val is None or val == "":
                errors.append(f"Missing required field: {field}")

        # 2. Date checks
        open_date = record.get("open_date")
        close_date = record.get("close_date")
        if open_date and close_date:
            if isinstance(open_date, (date, str)) and isinstance(close_date, (date, str)):
                if str(open_date) > str(close_date):
                    errors.append("open_date must be before or equal to close_date")
            else:
                errors.append("open_date and close_date must be date objects or valid date strings")


        # 3. Enum validations
        status = record.get("status")
        if status and status not in [e.value for e in IPOStatus]:
            errors.append(f"Invalid status value: {status}")

        exchange = record.get("exchange")
        if exchange and exchange not in [e.value for e in IPOExchange]:
            errors.append(f"Invalid exchange value: {exchange}")

        ipo_type = record.get("ipo_type")
        if ipo_type and ipo_type not in [e.value for e in IPOType]:
            errors.append(f"Invalid ipo_type value: {ipo_type}")

        # 4. Numeric validation
        lot_size = record.get("lot_size")
        if lot_size is not None:
            try:
                val = int(lot_size)
                if val <= 0:
                    errors.append("lot_size must be a positive integer")
            except (ValueError, TypeError):
                errors.append("lot_size must be a valid integer")

        # 5. Warnings (non-blocking)
        if not record.get("company_overview"):
            warnings.append("No company_overview provided - AI quality may be reduced")
        if not record.get("financial_summary"):
            warnings.append("No financial_summary provided - AI scoring may be restricted")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
