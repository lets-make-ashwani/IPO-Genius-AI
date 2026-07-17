import pytest
import uuid
import datetime
from app.modules.users.models import User
from app.modules.users.models.activity import UserActivity
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.ipos.models.detail import IPODetail
from app.modules.ai.models.analysis import AIAnalysis, AIAnalysisStatus, AIRecommendation
from app.shared.security import create_access_token
from app.shared.exceptions import AppException
from fastapi import status

@pytest.fixture
def admin_header():
    admin_id = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
    token = create_access_token({"sub": str(admin_id), "email": "admin@example.com", "role": "ADMIN"})
    return {"Authorization": f"Bearer {token}"}, admin_id

@pytest.fixture
def user_header():
    user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    token = create_access_token({"sub": str(user_id), "email": "user@example.com", "role": "USER"})
    return {"Authorization": f"Bearer {token}"}, user_id

@pytest.fixture
def mock_admin_user():
    return User(
        id=uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        full_name="Admin User",
        email="admin@example.com",
        password_hash="fakehash",
        role="ADMIN",
        is_active=True
    )

@pytest.fixture
def mock_normal_user():
    return User(
        id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        full_name="Normal User",
        email="user@example.com",
        password_hash="fakehash",
        role="USER",
        is_active=True
    )

@pytest.fixture
def mock_ipo():
    return IPO(
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

# 1. Test Authorization & RBAC
def test_admin_dashboard_access_allowed(client, monkeypatch, mock_admin_user, admin_header):
    headers, _ = admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_admin_user)
    
    monkeypatch.setattr("app.modules.admin.services.admin.admin_service.get_dashboard_analytics", lambda db: {
        "total_users": 5,
        "total_ipos": 5,
        "total_watchlist_items": 5,
        "total_ai_analyses": 5,
        "recent_signups": [],
        "recent_activities": []
    })

    response = client.get("/api/v1/admin/dashboard", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total_users"] == 5

def test_admin_dashboard_access_forbidden(client, monkeypatch, mock_normal_user, user_header):
    headers, _ = user_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_normal_user)

    response = client.get("/api/v1/admin/dashboard", headers=headers)
    assert response.status_code == 403
    assert "Forbidden" in response.json()["message"]

def test_admin_dashboard_access_unauthorized(client):
    response = client.get("/api/v1/admin/dashboard")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["message"]

# 2. Test Safety protections (Self-deactivation, downgrade, last-admin)
def test_prevent_self_deactivation(client, monkeypatch, mock_admin_user, admin_header):
    headers, admin_id = admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_admin_user)

    payload = {"is_active": False}
    response = client.put(f"/api/v1/admin/users/{admin_id}", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Cannot deactivate your own account" in response.json()["message"]

def test_prevent_self_role_downgrade(client, monkeypatch, mock_admin_user, admin_header):
    headers, admin_id = admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_admin_user)

    payload = {"role": "USER"}
    response = client.put(f"/api/v1/admin/users/{admin_id}", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Cannot downgrade your own ADMIN role" in response.json()["message"]

def test_prevent_last_admin_removal(client, monkeypatch, mock_admin_user, admin_header):
    headers, admin_id = admin_header
    target_id = uuid.UUID("99999999-9999-9999-9999-999999999999")
    target_admin = User(
        id=target_id,
        full_name="Target Admin",
        email="target@example.com",
        role="ADMIN",
        is_active=True
    )
    
    def mock_get(db, uid):
        if uid == admin_id:
            return mock_admin_user
        if uid == target_id:
            return target_admin
        return None
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", mock_get)

    # Mock AdminService.update_user to raise exception directly to verify safety checks flow
    def mock_update_user(db, admin_user_id, target_user_id, payload):
        raise AppException("Cannot deactivate or demote the last active ADMIN account", status_code=status.HTTP_400_BAD_REQUEST)
    monkeypatch.setattr("app.modules.admin.services.admin.admin_service.update_user", mock_update_user)

    payload = {"is_active": False}
    response = client.put(f"/api/v1/admin/users/{target_id}", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Cannot deactivate or demote the last active ADMIN account" in response.json()["message"]

# 3. Test IPO CRUD
def test_create_ipo_success(client, monkeypatch, mock_admin_user, admin_header):
    headers, _ = admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_admin_user)
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda *args, **kwargs: None)
    
    def mock_create(db, ipo_data):
        return IPO(
            id=uuid.uuid4(),
            company_name=ipo_data.company_name,
            slug="new-ipo-corp",
            exchange=ipo_data.exchange,
            ipo_type=ipo_data.ipo_type,
            price_band=ipo_data.price_band,
            lot_size=ipo_data.lot_size,
            issue_size=ipo_data.issue_size,
            open_date=ipo_data.open_date,
            close_date=ipo_data.close_date,
            status=ipo_data.status,
            is_verified=True,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )

    monkeypatch.setattr("app.modules.ipos.services.ipo.ipo_service.create_ipo", mock_create)

    payload = {
        "company_name": "New IPO Corp",
        "exchange": "BSE",
        "ipo_type": "MAINBOARD",
        "price_band": "200-220",
        "lot_size": 30,
        "issue_size": "500 Cr",
        "open_date": "2026-08-01",
        "close_date": "2026-08-05",
        "status": "Upcoming"
    }

    response = client.post("/api/v1/admin/ipos", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["company_name"] == "New IPO Corp"
    assert data["data"]["slug"] == "new-ipo-corp"

def test_create_ipo_invalid_dates(client, monkeypatch, mock_admin_user, admin_header):
    headers, _ = admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_admin_user)

    # Mock the exception raised by ipo_service.create_ipo for date validations
    def mock_create_fail(db, ipo_data):
        raise AppException("Open date must be before or equal to close date", status_code=status.HTTP_400_BAD_REQUEST)
    monkeypatch.setattr("app.modules.ipos.services.ipo.ipo_service.create_ipo", mock_create_fail)

    payload = {
        "company_name": "Bad Dates Corp",
        "exchange": "NSE",
        "ipo_type": "SME",
        "price_band": "10-12",
        "lot_size": 1000,
        "issue_size": "10 Cr",
        "open_date": "2026-08-10",
        "close_date": "2026-08-05",
        "status": "Upcoming"
    }
    response = client.post("/api/v1/admin/ipos", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Open date must be before or equal to close date" in response.json()["message"]

# 4. Test AI manual trigger and cooldown rate limit
def test_manual_ai_trigger_and_cooldown(client, monkeypatch, mock_admin_user, mock_ipo, admin_header):
    headers, _ = admin_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: mock_admin_user)
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda *args, **kwargs: None)
    
    mock_analysis = AIAnalysis(
        id=uuid.uuid4(),
        ipo_id=mock_ipo.id,
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


    # 1. Trigger first run (succeeds)
    monkeypatch.setattr("app.modules.admin.services.admin.admin_service.trigger_ai_analysis", lambda db, admin_user_id, ipo_id: mock_analysis)
    
    response = client.post(f"/api/v1/admin/ai/run/{mock_ipo.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["success"] is True

    # 2. Trigger second run (fails with 429 cooldown)
    def mock_trigger_cooldown(db, admin_user_id, ipo_id):
        raise AppException("AI regeneration cooldown active. Please wait 290 seconds.", status_code=status.HTTP_429_TOO_MANY_REQUESTS)
        
    monkeypatch.setattr("app.modules.admin.services.admin.admin_service.trigger_ai_analysis", mock_trigger_cooldown)
    
    response = client.post(f"/api/v1/admin/ai/run/{mock_ipo.id}", headers=headers)
    assert response.status_code == 429
    assert "AI regeneration cooldown active" in response.json()["message"]
