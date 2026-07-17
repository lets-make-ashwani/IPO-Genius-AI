import pytest
import json
import uuid
import datetime
from app.modules.notifications.models.notification import (
    Notification,
    NotificationPreference,
    NotificationEventType,
    NotificationPriority,
    NotificationStatus
)

@pytest.fixture
def auth_header():
    user_id = uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")
    from app.shared.security import create_access_token
    token = create_access_token({"sub": str(user_id), "email": "jane@example.com", "role": "USER"})
    return {"Authorization": f"Bearer {token}"}, user_id

def test_verify_notifications_endpoints_trace(client, monkeypatch, auth_header):
    headers, _ = auth_header
    
    from app.modules.users.models.user import User
    user = User(
        id=uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        full_name="Jane Doe",
        email="jane@example.com",
        password_hash="fakehash",
        role="USER",
        is_active=True
    )

    pref = NotificationPreference(
        id=uuid.uuid4(),
        user_id=user.id,
        in_app_enabled=True,
        email_enabled=True,
        push_enabled=True,
        telegram_enabled=False,
        whatsapp_enabled=False,
        event_preferences={
            "IPO_UPDATES": True,
            "AI_ANALYSIS": True,
            "WATCHLIST": True
        }
    )

    notification = Notification(
        id=uuid.UUID("6517cbaa-ab6a-4a5c-b6dd-f09bb810a33d"),
        user_id=user.id,
        title="IPO Opened",
        message="A new IPO has opened today",
        event_type=NotificationEventType.IPO_OPEN,
        priority=NotificationPriority.NORMAL,
        status=NotificationStatus.UNREAD,
        is_read=False,
        context_metadata={"ipo_id": "test-ipo-uuid"},
        action_label="View IPO",
        action_url="/ipo/test-ipo-uuid",
        expires_at=None,
        deleted_at=None,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc),
        user=user
    )

    # Apply Monkeypatches
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: user)
    monkeypatch.setattr("app.modules.notifications.repositories.preference.preference_repository.get_by_user", lambda db, uid: pref)
    monkeypatch.setattr("app.modules.notifications.repositories.preference.preference_repository.update", lambda db, p: p)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.list_by_user", lambda db, user_id, status_filter, limit, offset: ([notification], 1))
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.count_unread", lambda db, uid: 1)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.get_by_id", lambda db, nid: notification)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.update", lambda db, n: n)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.mark_all_as_read", lambda db, uid: 1)
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda db, user_id, action, metadata_json: None)

    print("\n==================================================")
    print("VERIFYING NOTIFICATIONS MODULE ENDPOINTS")
    print("==================================================")

    # 1. Verify GET /notifications/preferences
    print("\n--- 1. GET /api/v1/notifications/preferences ---")
    res = client.get("/api/v1/notifications/preferences", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 2. Verify PUT /notifications/preferences
    payload_update = {
        "email_enabled": False,
        "event_preferences": {
            "WATCHLIST": False
        }
    }
    print("\n--- 2. PUT /api/v1/notifications/preferences ---")
    res = client.put("/api/v1/notifications/preferences", json=payload_update, headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 3. Verify GET /notifications
    print("\n--- 3. GET /api/v1/notifications ---")
    res = client.get("/api/v1/notifications", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 4. Verify GET /notifications/count
    print("\n--- 4. GET /api/v1/notifications/count ---")
    res = client.get("/api/v1/notifications/count", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 5. Verify PUT /notifications/{id}/read
    print("\n--- 5. PUT /api/v1/notifications/{id}/read ---")
    res = client.put(f"/api/v1/notifications/{notification.id}/read", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    # 6. Verify POST /notifications/read-all
    print("\n--- 6. POST /api/v1/notifications/read-all ---")
    res = client.post("/api/v1/notifications/read-all", headers=headers)
    print(f"Status Code: {res.status_code}")
    print("Response Body:", json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n==================================================")
    print("VERIFICATION COMPLETED")
    print("==================================================")
