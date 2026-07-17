import pytest
import uuid
import datetime
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.ipos.models.detail import IPODetail
from app.modules.ai.models.analysis import AIAnalysis, AIAnalysisStatus, AIRecommendation
from app.modules.ai.services.analysis import ai_analysis_service

@pytest.fixture
def test_ipo_with_detail():
    ipo_id = uuid.uuid4()
    ipo = IPO(
        id=ipo_id,
        company_name="AI Tech Ltd",
        slug="ai-tech-ltd",
        logo_url="https://example.com/logo.png",
        sector="Technology",
        industry="SaaS Solutions",
        exchange=IPOExchange.BOTH,
        ipo_type=IPOType.MAINBOARD,
        price_band="₹200 - ₹210",
        lot_size=70,
        issue_size="₹500 Cr",
        open_date=datetime.date(2026, 7, 20),
        close_date=datetime.date(2026, 7, 23),
        listing_date=datetime.date(2026, 7, 30),
        status=IPOStatus.OPEN,
        drhp_url="https://example.com/drhp",
        is_verified=True,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )
    details = IPODetail(
        id=uuid.uuid4(),
        ipo_id=ipo_id,
        company_overview="An AI and ML development company.",
        business_model="B2B Subscription.",
        promoters="Dr. AI",
        objectives="Growth capital.",
        financial_summary="Net profit margin 18%."
    )
    ipo.details = details
    return ipo

@pytest.fixture
def mock_ai_analysis(test_ipo_with_detail):
    return AIAnalysis(
        id=uuid.uuid4(),
        ipo_id=test_ipo_with_detail.id,
        is_active=True,
        version=1,
        status=AIAnalysisStatus.COMPLETED,
        summary="A positive summary.",
        business_analysis="SaaS business.",
        financial_analysis="Strong financials.",
        risk_analysis="Low risk.",
        management_analysis="Competent management.",
        valuation_analysis="Fairly priced.",
        industry_analysis="Growing sector.",
        financial_score=85,
        management_score=80,
        industry_score=75,
        risk_score=70,
        valuation_score=72,
        overall_score=76,
        confidence_score=0.88,
        confidence_reason="Audited balance sheets.",
        recommendation=AIRecommendation.SUBSCRIBE,
        source_hash=ai_analysis_service.calculate_ipo_hash(test_ipo_with_detail),
        provider="MOCK",
        model_name="mock-llm-v1",
        is_cached=True,
        cache_expires_at=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )

def test_get_ai_analysis_generation_on_missing(client, mock_db, test_ipo_with_detail):
    mock_db.query().options().filter().first.return_value = test_ipo_with_detail
    mock_db.query().filter().first.return_value = None
    mock_db.query().filter().update.return_value = 1
    mock_db.query().filter().scalar.return_value = 0

    response = client.get(f"/api/v1/ai/analysis/{test_ipo_with_detail.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "COMPLETED"
    assert data["data"]["overall_score"] == 76
    assert data["data"]["recommendation"] == "Subscribe"

def test_get_ai_analysis_cached_hit(client, mock_db, test_ipo_with_detail, mock_ai_analysis):
    mock_db.query().options().filter().first.return_value = test_ipo_with_detail
    mock_db.query().filter().first.return_value = mock_ai_analysis

    response = client.get(f"/api/v1/ai/analysis/{test_ipo_with_detail.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["is_cached"] is True
    assert data["data"]["version"] == 1

def test_regenerate_ai_analysis(client, mock_db, test_ipo_with_detail):
    mock_db.query().options().filter().first.return_value = test_ipo_with_detail
    mock_db.query().filter().update.return_value = 1
    mock_db.query().filter().scalar.return_value = 1

    response = client.post(f"/api/v1/ai/analysis/{test_ipo_with_detail.id}/regenerate")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["version"] == 2
    assert data["data"]["status"] == "COMPLETED"

def test_get_ai_summary(client, mock_db, test_ipo_with_detail, mock_ai_analysis):
    mock_db.query().options().filter().first.return_value = test_ipo_with_detail
    mock_db.query().filter().first.return_value = mock_ai_analysis

    response = client.get(f"/api/v1/ai/summary/{test_ipo_with_detail.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["summary"] == "A positive summary."
    assert data["data"]["overall_score"] == 76

def test_get_ai_score(client, mock_db, test_ipo_with_detail, mock_ai_analysis):
    mock_db.query().options().filter().first.return_value = test_ipo_with_detail
    mock_db.query().filter().first.return_value = mock_ai_analysis

    response = client.get(f"/api/v1/ai/score/{test_ipo_with_detail.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["financial_score"] == 85
    assert data["data"]["confidence_score"] == 0.88
    assert data["data"]["recommendation"] == "Subscribe"

def test_get_ai_risk(client, mock_db, test_ipo_with_detail, mock_ai_analysis):
    mock_db.query().options().filter().first.return_value = test_ipo_with_detail
    mock_db.query().filter().first.return_value = mock_ai_analysis

    response = client.get(f"/api/v1/ai/risk/{test_ipo_with_detail.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["risk_analysis"] == "Low risk."
    assert data["data"]["risk_score"] == 70
