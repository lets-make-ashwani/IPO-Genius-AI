import pytest
import uuid
import datetime
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.watchlist.models.watchlist import WatchlistFolder, WatchlistItem, WatchlistPriority
from app.modules.ai.models.analysis import AIAnalysis, AIAnalysisStatus, AIRecommendation
from app.shared.security import create_access_token

@pytest.fixture
def auth_header():
    user_id = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
    token = create_access_token({"sub": str(user_id), "email": "jane@example.com", "role": "USER"})
    return {"Authorization": f"Bearer {token}"}, user_id

@pytest.fixture
def test_user_fixture():
    from app.modules.users.models.user import User
    return User(
        id=uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        full_name="Jane Doe",
        email="jane@example.com",
        password_hash="fakehash",
        role="USER",
        is_active=True
    )

@pytest.fixture
def test_ipo_fixture():
    return IPO(
        id=uuid.UUID("9a912bb3-12cd-4034-bc23-a5c67890ef99"),
        company_name="Genius Tech Ltd",
        slug="genius-tech-ltd",
        logo_url="https://example.com/logo.png",
        sector="Technology",
        industry="Software Services",
        exchange=IPOExchange.BOTH,
        ipo_type=IPOType.MAINBOARD,
        price_band="₹100 - ₹105",
        lot_size=140,
        issue_size="₹1,500 Cr",
        open_date=datetime.date(2026, 7, 20),
        close_date=datetime.date(2026, 7, 23),
        listing_date=datetime.date(2026, 7, 30),
        status=IPOStatus.OPEN,
        is_verified=True,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )

@pytest.fixture
def test_folder_fixture(test_user_fixture):
    return WatchlistFolder(
        id=uuid.uuid4(),
        user_id=test_user_fixture.id,
        name="Default",
        color="#000000",
        is_default=True
    )

@pytest.fixture
def test_item_fixture(test_folder_fixture, test_ipo_fixture):
    return WatchlistItem(
        id=uuid.uuid4(),
        folder_id=test_folder_fixture.id,
        ipo_id=test_ipo_fixture.id,
        notes="Notes 123",
        tags=["Long Term"],
        priority=WatchlistPriority.HIGH,
        reminder_enabled=False,
        ai_overall_score=76,
        ai_recommendation="Subscribe",
        ai_confidence_score=0.88,
        deleted_at=None,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc),
        folder=test_folder_fixture,
        ipo=test_ipo_fixture
    )

@pytest.fixture
def mock_ai_analysis_fixture(test_ipo_fixture):
    return AIAnalysis(
        id=uuid.uuid4(),
        ipo_id=test_ipo_fixture.id,
        is_active=True,
        version=1,
        status=AIAnalysisStatus.COMPLETED,
        overall_score=76,
        confidence_score=0.88,
        recommendation=AIRecommendation.SUBSCRIBE
    )

# 1. Add to Watchlist
def test_add_to_watchlist_success(client, monkeypatch, test_user_fixture, test_ipo_fixture, test_folder_fixture, mock_ai_analysis_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.ipos.repositories.ipo.ipo_repository.get_by_id", lambda db, ipo_id: test_ipo_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_default_folder", lambda db, uid: test_folder_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_active_by_folder_and_ipo", lambda db, fid, ipo_id: None)
    monkeypatch.setattr("app.modules.ai.repositories.analysis.ai_analysis_repository.get_active_by_ipo_id", lambda db, ipo_id: mock_ai_analysis_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.create_item", lambda db, item: item)
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda db, user_id, action, metadata_json: None)

    payload = {
        "ipo_id": str(test_ipo_fixture.id),
        "notes": "Will apply only if GMP > 25%",
        "tags": ["Long Term", "High Risk"],
        "priority": "HIGH"
    }

    response = client.post("/api/v1/watchlist", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["notes"] == "Will apply only if GMP > 25%"
    assert data["data"]["ai_overall_score"] == 76
    assert data["data"]["ai_recommendation"] == "Subscribe"

def test_add_to_watchlist_duplicate(client, monkeypatch, test_user_fixture, test_ipo_fixture, test_folder_fixture, test_item_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.ipos.repositories.ipo.ipo_repository.get_by_id", lambda db, ipo_id: test_ipo_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_default_folder", lambda db, uid: test_folder_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_active_by_folder_and_ipo", lambda db, fid, ipo_id: test_item_fixture)

    payload = {"ipo_id": str(test_ipo_fixture.id)}
    response = client.post("/api/v1/watchlist", json=payload, headers=headers)
    assert response.status_code == 400
    assert "already in watchlist" in response.json()["message"]

# 2. Update Watchlist Item
def test_update_watchlist_item(client, monkeypatch, test_user_fixture, test_item_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_item_by_id", lambda db, item_id: test_item_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.update_item", lambda db, item: item)

    payload = {
        "notes": "Updated Notes",
        "priority": "LOW",
        "reminder_enabled": True,
        "reminder_date": "2026-07-19T10:00:00Z"
    }
    response = client.put(f"/api/v1/watchlist/items/{test_item_fixture.id}", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["notes"] == "Updated Notes"
    assert data["data"]["priority"] == "LOW"

# 3. Soft Delete
def test_remove_from_watchlist(client, monkeypatch, test_user_fixture, test_folder_fixture, test_item_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_default_folder", lambda db, uid: test_folder_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_active_by_folder_and_ipo", lambda db, fid, ipo_id: test_item_fixture)
    
    def mock_soft_delete(db, item):
        item.deleted_at = datetime.datetime.now(datetime.timezone.utc)
        return item
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.soft_delete_item", mock_soft_delete)
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda db, user_id, action, metadata_json: None)

    response = client.delete(f"/api/v1/watchlist/{test_item_fixture.ipo_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert test_item_fixture.deleted_at is not None

# 4. List Watchlist
def test_get_watchlist_list(client, monkeypatch, test_user_fixture, test_folder_fixture, test_item_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_default_folder", lambda db, uid: test_folder_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.list_active_by_folder", lambda db, folder_id, sort_by, status_filter, sector_filter, industry_filter, ipo_type_filter, rec_filter, limit, offset: ([test_item_fixture], 1))

    response = client.get("/api/v1/watchlist?sort_by=Newest&limit=10&offset=0", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["notes"] == "Notes 123"
    assert data["data"][0]["ipo"]["company_name"] == "Genius Tech Ltd"

# 5. Summary and Count
def test_get_watchlist_summary(client, monkeypatch, test_user_fixture, test_folder_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_default_folder", lambda db, uid: test_folder_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.count_active_by_folder", lambda db, folder_id: 5)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_status_distribution", lambda db, folder_id: {"Open": 2, "Upcoming": 3})

    response = client.get("/api/v1/watchlist/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total_count"] == 5
    assert data["data"]["open_count"] == 2
    assert data["data"]["upcoming_count"] == 3

def test_get_watchlist_count(client, monkeypatch, test_user_fixture, test_folder_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_default_folder", lambda db, uid: test_folder_fixture)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.count_active_by_folder", lambda db, folder_id: 3)

    response = client.get("/api/v1/watchlist/count", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["count"] == 3

# 6. Unauthorized Check
def test_watchlist_unauthorized(client):
    response = client.get("/api/v1/watchlist")
    assert response.status_code == 401
