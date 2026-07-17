import pytest
import uuid
import datetime
from app.modules.notifications.models.notification import (
    Notification,
    NotificationPreference,
    NotificationEventType,
    NotificationPriority,
    NotificationStatus
)
from app.modules.notifications.events.dispatcher import event_dispatcher
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
def test_pref_fixture(test_user_fixture):
    return NotificationPreference(
        id=uuid.uuid4(),
        user_id=test_user_fixture.id,
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

@pytest.fixture
def test_notification_fixture(test_user_fixture):
    return Notification(
        id=uuid.uuid4(),
        user_id=test_user_fixture.id,
        title="IPO Opened",
        message="A new IPO has opened today",
        event_type=NotificationEventType.IPO_OPEN,
        priority=NotificationPriority.NORMAL,
        status=NotificationStatus.UNREAD,
        is_read=False,
        context_metadata={"ipo_id": "some-uuid"},
        action_label="View IPO",
        action_url="/ipo/some-uuid",
        expires_at=None,
        deleted_at=None,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )

# 1. Preferences retrieve & update
def test_get_preferences(client, monkeypatch, test_user_fixture, test_pref_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.notifications.repositories.preference.preference_repository.get_by_user", lambda db, uid: test_pref_fixture)

    response = client.get("/api/v1/notifications/preferences", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["in_app_enabled"] is True
    assert data["data"]["event_preferences"]["IPO_UPDATES"] is True

def test_update_preferences(client, monkeypatch, test_user_fixture, test_pref_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.notifications.repositories.preference.preference_repository.get_by_user", lambda db, uid: test_pref_fixture)
    monkeypatch.setattr("app.modules.notifications.repositories.preference.preference_repository.update", lambda db, pref: pref)

    payload = {
        "email_enabled": False,
        "event_preferences": {
            "AI_ANALYSIS": False
        }
    }
    response = client.put("/api/v1/notifications/preferences", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email_enabled"] is False
    assert data["data"]["event_preferences"]["AI_ANALYSIS"] is False

# 2. Event Dispatching & Rules engine persistence
def test_event_dispatch_creates_notification(client, monkeypatch, test_user_fixture, test_pref_fixture):
    monkeypatch.setattr("app.modules.notifications.repositories.preference.preference_repository.get_by_user", lambda db, uid: test_pref_fixture)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.check_duplicate_exists", lambda db, user_id, event_type, match_metadata, window_minutes: False)
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda db, user_id, action, metadata_json: None)

    created_notifications = []
    def mock_create(db, notification):
        created_notifications.append(notification)
        return notification
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.create", mock_create)

    # Trigger decoupled event dispatcher
    event_dispatcher.dispatch(
        "NOTIFICATION_TRIGGER",
        db=None,
        user_id=test_user_fixture.id,
        title="AI Analysis Done",
        message="AI report completed",
        event_type=NotificationEventType.AI_ANALYSIS_COMPLETED,
        priority=NotificationPriority.HIGH,
        context_metadata={"ipo_id": "test-ipo-uuid"}
    )

    assert len(created_notifications) == 1
    assert created_notifications[0].title == "AI Analysis Done"
    assert created_notifications[0].priority == NotificationPriority.HIGH
    assert created_notifications[0].status == NotificationStatus.UNREAD

# 3. Duplicate Suppression check
def test_duplicate_suppression(client, monkeypatch, test_user_fixture, test_pref_fixture):
    monkeypatch.setattr("app.modules.notifications.repositories.preference.preference_repository.get_by_user", lambda db, uid: test_pref_fixture)
    # Mock check_duplicate_exists to return True
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.check_duplicate_exists", lambda db, user_id, event_type, match_metadata, window_minutes: True)

    created_notifications = []
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.create", lambda db, n: created_notifications.append(n))

    event_dispatcher.dispatch(
        "NOTIFICATION_TRIGGER",
        db=None,
        user_id=test_user_fixture.id,
        title="Spam Message",
        message="Spam",
        event_type=NotificationEventType.SYSTEM_NOTIFICATION
    )
    assert len(created_notifications) == 0  # Should be suppressed!

# 4. APIs Listing, Reads & Counts
def test_get_notifications_list(client, monkeypatch, test_user_fixture, test_notification_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.list_by_user", lambda db, user_id, status_filter, limit, offset: ([test_notification_fixture], 1))

    response = client.get("/api/v1/notifications?status=UNREAD&limit=10&offset=0", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["title"] == "IPO Opened"
    assert data["data"][0]["is_read"] is False

def test_mark_as_read(client, monkeypatch, test_user_fixture, test_notification_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.get_by_id", lambda db, nid: test_notification_fixture)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.update", lambda db, n: n)
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda db, user_id, action, metadata_json: None)

    response = client.put(f"/api/v1/notifications/{test_notification_fixture.id}/read", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "READ"
    assert data["data"]["is_read"] is True

def test_mark_all_as_read(client, monkeypatch, test_user_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.mark_all_as_read", lambda db, uid: 3)
    monkeypatch.setattr("app.modules.users.repositories.activity.user_activity_repository.log_activity", lambda db, user_id, action, metadata_json: None)

    response = client.post("/api/v1/notifications/read-all", headers=headers)
    assert response.status_code == 200
    assert "Successfully marked 3 notifications as read" in response.json()["message"]

def test_get_unread_count(client, monkeypatch, test_user_fixture, auth_header):
    headers, _ = auth_header
    monkeypatch.setattr("app.modules.users.repositories.user.user_repository.get_by_id", lambda db, uid: test_user_fixture)
    monkeypatch.setattr("app.modules.notifications.repositories.notification.notification_repository.count_unread", lambda db, uid: 4)

    response = client.get("/api/v1/notifications/count", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["count"] == 4

def test_notifications_unauthorized(client):
    response = client.get("/api/v1/notifications")
    assert response.status_code == 401
