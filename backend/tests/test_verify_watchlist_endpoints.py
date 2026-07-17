import pytest
import json
import uuid
import datetime
from app.modules.ipos.models.ipo import IPO, IPOStatus, IPOExchange, IPOType
from app.modules.watchlist.models.watchlist import WatchlistFolder, WatchlistItem, WatchlistPriority
from app.modules.ai.models.analysis import AIAnalysis, AIAnalysisStatus, AIRecommendation

@pytest.fixture
def auth_header():
    user_id = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
    from app.shared.security import create_access_token
    token = create_access_token({"sub": str(user_id), "email": "jane@example.com", "role": "USER"})
    return {"Authorization": f"Bearer {token}"}, user_id

def test_verify_watchlist_endpoints_trace(client, monkeypatch, auth_header):
    headers, _ = auth_header
    ipo_id = uuid.UUID("9a912bb3-12cd-4034-bc23-a5c67890ef99")
    
    from app.modules.users.models.user import User
    user = User(
        id=uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        full_name="Jane Doe",
        email="jane@example.com",
        password_hash="fakehash",
        role="USER",
        is_active=True
    )

    ipo = IPO(
        id=ipo_id,
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

    folder = WatchlistFolder(
        id=uuid.UUID("d3b07384-d113-4c9f-b98a-13008064baef"),
        user_id=user.id,
        name="Default",
        color="#000000",
        is_default=True
    )

    item = WatchlistItem(
        id=uuid.UUID("44c4b66b-4df2-4752-b883-9993e3d1c448"),
        folder_id=folder.id,
        ipo_id=ipo_id,
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
        folder=folder,
        ipo=ipo
    )

    # Apply Monkeypatches
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: user)
    monkeypatch.setattr("app.modules.ipos.repositories.ipo.ipo_repository.get_by_id", lambda db, ipo_id: ipo)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_default_folder", lambda db, uid: folder)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_active_by_folder_and_ipo", lambda db, fid, ipo_id: item)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_item_by_id", lambda db, item_id: item)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.update_item", lambda db, item: item)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.soft_delete_item", lambda db, item: item)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.list_active_by_folder", lambda db, folder_id, sort_by, status_filter, sector_filter, industry_filter, ipo_type_filter, rec_filter, limit, offset: ([item], 1))
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.count_active_by_folder", lambda db, folder_id: 1)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_status_distribution", lambda db, folder_id: {"Open": 1})
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda db, user_id, action, metadata_json: None)
    monkeypatch.setattr("app.modules.ai.repositories.analysis.ai_analysis_repository.get_active_by_ipo_id", lambda db, ipo_id: None)

    print("\n==================================================")
    print("VERIFYING WATCHLIST MODULE ENDPOINTS")
    print("==================================================")

    # 1. Verify POST /watchlist
    # Temporary patch for add (needs get_active_by_folder_and_ipo to return None, then we restore)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_active_by_folder_and_ipo", lambda db, fid, ipo_id: None)
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.create_item", lambda db, item: item)
    payload = {
        "ipo_id": str(ipo_id),
        "notes": "Will apply only if GMP > 25%",
        "tags": ["Long Term"],
        "priority": "HIGH"
    }
    print("\n--- 1. POST /api/v1/watchlist ---")
    res = client.post("/api/v1/watchlist", json=payload, headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 201

    # Restore patch
    monkeypatch.setattr("app.modules.watchlist.repositories.watchlist.watchlist_repository.get_active_by_folder_and_ipo", lambda db, fid, ipo_id: item)

    # 2. Verify PUT /watchlist/items/{item_id}
    payload_update = {
        "notes": "Updated Note Text",
        "priority": "LOW"
    }
    print("\n--- 2. PUT /api/v1/watchlist/items/{item_id} ---")
    res = client.put(f"/api/v1/watchlist/items/{item.id}", json=payload_update, headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 3. Verify GET /watchlist
    print("\n--- 3. GET /api/v1/watchlist ---")
    res = client.get("/api/v1/watchlist", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 4. Verify GET /watchlist/summary
    print("\n--- 4. GET /api/v1/watchlist/summary ---")
    res = client.get("/api/v1/watchlist/summary", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 5. Verify GET /watchlist/count
    print("\n--- 5. GET /api/v1/watchlist/count ---")
    res = client.get("/api/v1/watchlist/count", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 6. Verify DELETE /watchlist/{ipo_id}
    print("\n--- 6. DELETE /api/v1/watchlist/{ipo_id} ---")
    res = client.delete(f"/api/v1/watchlist/{ipo_id}", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n==================================================")
    print("VERIFICATION COMPLETED")
    print("==================================================")
