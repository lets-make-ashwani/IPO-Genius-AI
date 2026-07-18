import pytest
import uuid
import datetime
from app.modules.pipeline.services.normalizer import Normalizer
from app.modules.pipeline.services.validator import IPODataValidator
from app.modules.pipeline.services.pipeline import PipelineService
from app.modules.pipeline.models.pipeline import (
    PipelineRun,
    PipelineRunItem,
    PipelineRunStatus,
    PipelineRunTrigger,
    PipelineItemStatus,
    PipelineItemStage,
)
from app.modules.ipos.models.ipo import IPOStatus, IPOExchange, IPOType

# 1. Test Normalizer
def test_normalizer_success():
    normalizer = Normalizer()
    raw = {
        "source_identifier": "  tech-2026  ",
        "company_name": "  Tech Corp Ltd  ",
        "price_band": "Rs 150 - Rs 160",
        "lot_size": " 120 ",
        "issue_size": "Rs. 400 Cr",
        "open_date": "2026-08-01",
        "close_date": "03-08-2026",
        "listing_date": None,
        "status": "upcoming_ipo",
        "exchange": "bse & nse",
        "ipo_type": "sme_ipo",
        "gmp": " 25 "
    }
    res = normalizer.normalize(raw)
    assert res["source_identifier"] == "tech-2026"
    assert res["company_name"] == "Tech Corp Ltd"
    assert res["price_band"] == "₹150 - Rs 160"
    assert res["lot_size"] == 120
    assert res["issue_size"] == "₹400 Cr"
    assert res["open_date"] == datetime.date(2026, 8, 1)
    assert res["close_date"] == datetime.date(2026, 8, 3)
    assert res["listing_date"] is None
    assert res["status"] == IPOStatus.UPCOMING.value
    assert res["exchange"] == IPOExchange.BOTH.value
    assert res["ipo_type"] == IPOType.SME.value
    assert res["gmp"] == 25

def test_normalizer_edge_cases():
    normalizer = Normalizer()
    raw = {
        "lot_size": "invalid",
        "gmp": "invalid_gmp",
        "open_date": "invalid-date",
        "status": "weird_status",
        "exchange": "BSE only",
        "price_band": None
    }
    res = normalizer.normalize(raw)
    assert res["lot_size"] == 0
    assert res["gmp"] is None
    assert res["open_date"] is None
    assert res["status"] == IPOStatus.UPCOMING.value
    assert res["exchange"] == IPOExchange.BSE.value
    assert res["price_band"] == ""

# 2. Test Validator
def test_validator_success():
    validator = IPODataValidator()
    valid_record = {
        "company_name": "Valid IPO Ltd",
        "price_band": "₹100 - ₹110",
        "lot_size": 150,
        "issue_size": "₹300 Cr",
        "open_date": datetime.date(2026, 8, 1),
        "close_date": datetime.date(2026, 8, 3),
        "status": "Upcoming",
        "exchange": "BSE & NSE",
        "ipo_type": "MAINBOARD"
    }
    res = validator.validate(valid_record)
    assert res["is_valid"] is True
    assert len(res["errors"]) == 0

def test_validator_failures():
    validator = IPODataValidator()
    # Missing required field, incorrect date order, non-positive lot size
    invalid_record = {
        "company_name": "",
        "price_band": "₹100",
        "lot_size": -10,
        "issue_size": "",
        "open_date": datetime.date(2026, 8, 5),
        "close_date": datetime.date(2026, 8, 3),
        "status": "Unknown",
        "exchange": "BSE & NSE",
        "ipo_type": "MAINBOARD"
    }
    res = validator.validate(invalid_record)
    assert res["is_valid"] is False
    assert any("company_name" in err for err in res["errors"])
    assert any("open_date" in err for err in res["errors"])
    assert any("lot_size" in err for err in res["errors"])

# 3. Test Service logic execution with Mocks
def test_pipeline_service_duplicate_idempotency_key(monkeypatch):
    service = PipelineService()
    run_id = uuid.uuid4()
    mock_run = PipelineRun(id=run_id, idempotency_key="dup_key")
    
    # Mock repo to return existing run
    monkeypatch.setattr(
        "app.modules.pipeline.repositories.pipeline.pipeline_run_repository.get_by_idempotency_key",
        lambda db, key: mock_run
    )
    
    from app.shared.exceptions import AppException
    with pytest.raises(AppException) as exc:
        service.execute_pipeline_run(
            db=None,
            provider_name="MOCK",
            trigger=PipelineRunTrigger.MANUAL,
            idempotency_key="dup_key"
        )
    assert exc.value.status_code == 409

def test_pipeline_service_runs_successfully(monkeypatch):
    service = PipelineService()
    
    from unittest.mock import MagicMock
    db = MagicMock()
    # Mock query chain to return None (no existing IPO found)
    db.query.return_value.filter.return_value.first.return_value = None
    db.query.return_value.filter.return_value.all.return_value = []
    
    # Mock repos
    monkeypatch.setattr(
        "app.modules.pipeline.repositories.pipeline.pipeline_run_repository.get_by_idempotency_key",
        lambda d, k: None
    )
    monkeypatch.setattr(
        "app.modules.pipeline.repositories.pipeline.pipeline_run_item_repository.count_by_status",
        lambda d, r_id: {PipelineItemStatus.COMPLETED: 1}
    )
    monkeypatch.setattr(
        "app.modules.ipos.repositories.ipo.ipo_repository.get_by_slug",
        lambda d, slug: None
    )
    
    # Mock external calls
    monkeypatch.setattr(
        "app.modules.pipeline.services.providers.mock_ipo_provider.MockIPODataProvider.discover_ipos",
        lambda self: [
            {
                "source_identifier": "mock-p1",
                "company_name": "Mock P1 Ltd",
                "price_band": "100-110",
                "lot_size": 100,
                "issue_size": "₹200 Cr",
                "open_date": "2026-08-01",
                "close_date": "2026-08-03",
                "listing_date": None,
                "status": "Upcoming",
                "exchange": "BSE & NSE",
                "ipo_type": "MAINBOARD",
                "sector": "Tech",
                "industry": "IT",
                "drhp_url": None,
                "rhp_url": None,
                "prospectus_url": None,
                "source_url": None,
                "gmp": 10,
                "company_overview": "Overview",
                "business_model": "Model",
                "promoters": "Promoters",
                "objectives": "Objectives",
                "financial_summary": "Financials"
            }
        ]
    )
    monkeypatch.setattr(
        "app.modules.ai.services.analysis.ai_analysis_service.generate_analysis",
        lambda d, ipo, async_generation: type("MockAnalysis", (), {
            "provider": "MOCK",
            "model_name": "mock-llm-v1",
            "tokens_used": 100,
            "processing_time_ms": 200
        })()
    )
    
    run = service.execute_pipeline_run(
        db=db,
        provider_name="MOCK",
        trigger=PipelineRunTrigger.MANUAL,
        idempotency_key="unique_key"
    )
    
    assert run.idempotency_key == "unique_key"
    assert run.status == PipelineRunStatus.COMPLETED
    assert run.total_discovered == 1
    assert run.total_processed == 1
