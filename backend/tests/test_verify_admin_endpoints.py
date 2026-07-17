import pytest
import json
import uuid
import datetime
from app.modules.users.models import User
from app.modules.users.models.activity import UserActivity
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.ipos.models.detail import IPODetail
from app.modules.ai.models.analysis import AIAnalysis, AIAnalysisStatus, AIRecommendation
from app.shared.security import create_access_token

@pytest.fixture
def admin_header():
    admin_id = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
    token = create_access_token({"sub": str(admin_id), "email": "admin@example.com", "role": "ADMIN"})
    return {"Authorization": f"Bearer {token}"}, admin_id

def test_verify_admin_endpoints_trace(client, monkeypatch, admin_header):
    headers, admin_id = admin_header

    user = User(
        id=admin_id,
        full_name="Admin User",
        email="admin@example.com",
        role="ADMIN",
        is_active=True,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )

    ipo = IPO(
        id=uuid.UUID("11111111-1111-1111-1111-111111111111"),
        company_name="Test Company",
        slug="test-company",
        exchange=IPOExchange.BSE,
        ipo_type=IPOType.MAINBOARD,
        price_band="100-120",
        lot_size=50,
        issue_size="100 Cr",
        open_date=datetime.date(2026, 7, 1),
        close_date=datetime.date(2026, 7, 5),
        status=IPOStatus.OPEN,
        is_verified=True,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc),
        details=IPODetail(
            id=uuid.uuid4(),
            company_overview="Overview",
            business_model="Model",
            promoters="Promoters",
            objectives="Objectives",
            financial_summary="Summary"
        )
    )

    analysis = AIAnalysis(
        id=uuid.UUID("55555555-5555-5555-5555-555555555555"),
        ipo_id=ipo.id,
        is_active=True,
        status=AIAnalysisStatus.COMPLETED,
        version=1,
        financial_score=80,
        management_score=85,
        industry_score=75,
        risk_score=70,
        valuation_score=75,
        overall_score=77,
        confidence_score=0.8,
        is_cached=True,
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        recommendation=AIRecommendation.SUBSCRIBE,
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )



    # Monkeypatching Database operations & Services
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: user)
    monkeypatch.setattr("app.modules.ipos.services.ipo.ipo_service.get_ipos", lambda db, limit, offset: ([ipo], 1))
    monkeypatch.setattr("app.modules.ipos.services.ipo.ipo_service.get_ipo_by_id", lambda db, ipo_id: ipo)
    monkeypatch.setattr("app.modules.ipos.services.ipo.ipo_service.create_ipo", lambda db, payload: ipo)
    monkeypatch.setattr("app.modules.ipos.services.ipo.ipo_service.update_ipo", lambda db, ipo_id, ipo_data: ipo)
    monkeypatch.setattr("app.modules.ipos.services.ipo.ipo_service.delete_ipo", lambda db, ipo_id: None)
    monkeypatch.setattr("app.modules.admin.services.admin.admin_service.get_dashboard_analytics", lambda db: {
        "total_users": 1,
        "total_ipos": 1,
        "total_watchlist_items": 0,
        "total_ai_analyses": 1,
        "recent_signups": [{"date": "2026-07-17", "count": 1}],
        "recent_activities": []
    })
    monkeypatch.setattr("app.modules.admin.services.admin.admin_service.list_users", lambda db, **kwargs: ([user], 1))
    monkeypatch.setattr("app.modules.admin.services.admin.admin_service.update_user", lambda db, **kwargs: user)
    monkeypatch.setattr("app.modules.admin.services.admin.admin_service.deactivate_user_account", lambda db, **kwargs: user)
    monkeypatch.setattr("app.modules.admin.services.admin.admin_service.trigger_ai_analysis", lambda db, **kwargs: analysis)
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda *args, **kwargs: None)

    print("\n==================================================")
    print("VERIFYING ADMIN PANEL ENDPOINTS")
    print("==================================================")

    # 1. GET /admin/dashboard
    print("\n--- 1. GET /api/v1/admin/dashboard ---")
    res = client.get("/api/v1/admin/dashboard", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 2. GET /admin/users
    print("\n--- 2. GET /api/v1/admin/users ---")
    res = client.get("/api/v1/admin/users?limit=5", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 3. PUT /admin/users/{id}
    print("\n--- 3. PUT /api/v1/admin/users/{user_id} ---")
    res = client.put(f"/api/v1/admin/users/{user.id}", json={"full_name": "Updated Admin Name"}, headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 4. GET /admin/ipos
    print("\n--- 4. GET /api/v1/admin/ipos ---")
    res = client.get("/api/v1/admin/ipos", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 5. POST /admin/ipos
    print("\n--- 5. POST /api/v1/admin/ipos ---")
    payload_ipo = {
        "company_name": "Test Company",
        "exchange": "BSE",
        "ipo_type": "MAINBOARD",
        "price_band": "100-120",
        "lot_size": 50,
        "issue_size": "100 Cr",
        "open_date": "2026-07-01",
        "close_date": "2026-07-05",
        "status": "Open"
    }
    res = client.post("/api/v1/admin/ipos", json=payload_ipo, headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 6. POST /admin/ai/run/{ipo_id}
    print("\n--- 6. POST /api/v1/admin/ai/run/{ipo_id} ---")
    res = client.post(f"/api/v1/admin/ai/run/{ipo.id}", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n==================================================")
    print("VERIFICATION COMPLETED")
    print("==================================================")
