import pytest
import uuid
import datetime
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.database.session import get_db
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.ipos.models.detail import IPODetail
from app.modules.ai.models.analysis import AIAnalysis

@pytest.fixture
def sample_ipo():
    ipo_id = uuid.UUID("3a921d01-e283-4921-987f-13d80a12001f")
    ipo = IPO(
        id=ipo_id,
        company_name="Swiggy Limited",
        slug="swiggy-limited",
        sector="FMCG & Quick Commerce",
        industry="Quick Commerce",
        exchange="NSE",
        ipo_type="MAINBOARD",
        price_band="₹371 - ₹390",
        lot_size=38,
        issue_size="11327 Cr",
        open_date=datetime.date(2024, 11, 6),
        close_date=datetime.date(2024, 11, 8),
        listing_date=datetime.date(2024, 11, 13),
        status="Listed",
        gmp=25,
        drhp_url="https://sebi.gov.in/swiggy_drhp.pdf",
        rhp_url="https://sebi.gov.in/swiggy_rhp.pdf",
        prospectus_url="https://sebi.gov.in/swiggy_prospectus.pdf",
        source="NSE",
        is_verified=True,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )
    details = IPODetail(
        id=uuid.uuid4(),
        ipo_id=ipo_id,
        company_overview="Swiggy is a leading quick commerce brand in India.",
        business_model="Hyper-local delivery platform",
        promoters="Prosus Group",
        objectives="Debt reduction and tech expansion",
        financial_summary="Revenue growth 24% YoY"
    )
    ipo.details = details
    return ipo

@pytest.fixture
def mock_db_session(sample_ipo):
    db = MagicMock()
    
    # Mock query chain for IPO & AIAnalysis queries
    def query_side_effect(model):
        query_mock = MagicMock()
        query_mock.options.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.order_by.return_value = query_mock
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock

        if model == AIAnalysis:
            sample_analysis = AIAnalysis(
                id=uuid.uuid4(),
                ipo_id=sample_ipo.id,
                overall_score=84,
                financial_score=88,
                management_score=82,
                valuation_score=79,
                risk_score=25,
                recommendation="SUBSCRIBE",
                summary="Swiggy Limited shows strong growth momentum.",
                structured_data={"strengths": ["Strong brand"], "weaknesses": ["Competition"], "risks": ["Policy"]},
                provider="GEMINI",
                model_name="gemini-1.5-flash"
            )
            query_mock.all.return_value = [sample_analysis]
            query_mock.first.return_value = sample_analysis
            query_mock.count.return_value = 1
        else:
            query_mock.all.return_value = [sample_ipo]
            query_mock.first.return_value = sample_ipo
            query_mock.count.return_value = 1
            
        return query_mock

    db.query.side_effect = query_side_effect
    return db


@pytest.fixture
def api_client(mock_db_session):
    def override_get_db():
        yield mock_db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

# --- Phase 3.1 Core IPO APIs Tests ---

def test_get_all_ipos(api_client):
    res = api_client.get("/api/v1/ipos")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert "data" in json_data
    assert "pagination" in json_data

def test_search_ipos(api_client):
    res = api_client.get("/api/v1/ipos/search?q=Swiggy")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert len(json_data["data"]) >= 1

def test_get_upcoming_ipos(api_client):
    res = api_client.get("/api/v1/ipos/upcoming")
    assert res.status_code == 200
    assert res.json()["success"] is True

def test_get_open_ipos(api_client):
    res = api_client.get("/api/v1/ipos/open")
    assert res.status_code == 200
    assert res.json()["success"] is True

def test_get_listed_ipos(api_client):
    res = api_client.get("/api/v1/ipos/listed")
    assert res.status_code == 200
    assert res.json()["success"] is True

def test_get_closed_ipos(api_client):
    res = api_client.get("/api/v1/ipos/closed")
    assert res.status_code == 200
    assert res.json()["success"] is True

def test_get_ipo_by_id_or_slug(api_client):
    res = api_client.get("/api/v1/ipos/swiggy-limited")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert json_data["data"]["company_name"] == "Swiggy Limited"

# --- Phase 3.2 Sub-resource APIs Tests ---

def test_get_ipo_analysis(api_client):
    res = api_client.get("/api/v1/ipos/swiggy-limited/analysis")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert "overall_score" in json_data["data"]
    assert "recommendation" in json_data["data"]

def test_get_ipo_financials(api_client):
    res = api_client.get("/api/v1/ipos/swiggy-limited/financials")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert "financial_summary" in json_data["data"]

def test_get_ipo_subscription(api_client):
    res = api_client.get("/api/v1/ipos/swiggy-limited/subscription")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert "total_subscription" in json_data["data"]

def test_get_ipo_documents(api_client):
    res = api_client.get("/api/v1/ipos/swiggy-limited/documents")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert "drhp_url" in json_data["data"]

def test_get_ipo_news(api_client):
    res = api_client.get("/api/v1/ipos/swiggy-limited/news")
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert len(json_data["data"]["articles"]) >= 1
