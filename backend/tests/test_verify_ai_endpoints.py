import pytest
import json
import uuid
import datetime
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.ipos.models.detail import IPODetail
from app.modules.ai.models.analysis import AIAnalysis, AIAnalysisStatus, AIRecommendation
from app.modules.ai.services.analysis import ai_analysis_service

def test_verify_ai_endpoints_trace(client, mock_db):
    ipo_id = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
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

    mock_analysis = AIAnalysis(
        id=uuid.uuid4(),
        ipo_id=ipo_id,
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
        source_hash=ai_analysis_service.calculate_ipo_hash(ipo),
        provider="MOCK",
        model_name="mock-llm-v1",
        is_cached=True,
        cache_expires_at=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )

    print("\n==================================================")
    print("VERIFYING AI ANALYSIS MODULE ENDPOINTS")
    print("==================================================")

    # 1. Verify GET /ai/analysis/{ipo_id}
    mock_db.query().options().filter().first.return_value = ipo
    mock_db.query().filter().first.return_value = mock_analysis
    print("\n--- 1. GET /api/v1/ai/analysis/{ipo_id} ---")
    res = client.get(f"/api/v1/ai/analysis/{ipo_id}")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 2. Verify GET /ai/summary/{ipo_id}
    mock_db.query().options().filter().first.return_value = ipo
    mock_db.query().filter().first.return_value = mock_analysis
    print("\n--- 2. GET /api/v1/ai/summary/{ipo_id} ---")
    res = client.get(f"/api/v1/ai/summary/{ipo_id}")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 3. Verify GET /ai/score/{ipo_id}
    mock_db.query().options().filter().first.return_value = ipo
    mock_db.query().filter().first.return_value = mock_analysis
    print("\n--- 3. GET /api/v1/ai/score/{ipo_id} ---")
    res = client.get(f"/api/v1/ai/score/{ipo_id}")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 4. Verify GET /ai/risk/{ipo_id}
    mock_db.query().options().filter().first.return_value = ipo
    mock_db.query().filter().first.return_value = mock_analysis
    print("\n--- 4. GET /api/v1/ai/risk/{ipo_id} ---")
    res = client.get(f"/api/v1/ai/risk/{ipo_id}")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 5. Verify POST /ai/analysis/{ipo_id}/regenerate
    mock_db.query().options().filter().first.return_value = ipo
    mock_db.query().filter().first.return_value = None
    mock_db.query().filter().update.return_value = 1
    mock_db.query().filter().scalar.return_value = 1
    print("\n--- 5. POST /api/v1/ai/analysis/{ipo_id}/regenerate ---")
    res = client.post(f"/api/v1/ai/analysis/{ipo_id}/regenerate")
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n==================================================")
    print("VERIFICATION COMPLETED")
    print("==================================================")
