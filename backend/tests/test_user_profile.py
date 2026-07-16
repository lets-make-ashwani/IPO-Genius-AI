import pytest
from unittest.mock import MagicMock
import uuid
from datetime import datetime, timezone
from app.modules.users.models.user import User
from app.modules.users.models.settings import UserSetting
from app.modules.users.models.activity import UserActivity, UserActivityType
from app.shared.security import create_access_token, get_password_hash

@pytest.fixture
def auth_header():
    user_id = uuid.uuid4()
    token = create_access_token({"sub": str(user_id), "email": "user@example.com", "role": "USER"})
    return {"Authorization": f"Bearer {token}"}, user_id

@pytest.fixture
def test_user(auth_header):
    _, user_id = auth_header
    return User(
        id=user_id,
        full_name="Alice Smith",
        email="user@example.com",
        password_hash=get_password_hash("password123"),
        avatar_url=None,
        role="USER",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

@pytest.fixture
def test_settings(test_user):
    return UserSetting(
        id=uuid.uuid4(),
        user_id=test_user.id,
        theme="light",
        language="en",
        timezone="UTC",
        currency="USD",
        email_notifications=True,
        push_notifications=True,
        marketing_emails=False,
        date_format="YYYY-MM-DD",
        time_format="24h",
        first_day_of_week=1
    )

def test_get_profile_success(client, mock_db, test_user, auth_header):
    headers, _ = auth_header
    mock_db.query().filter().first.return_value = test_user

    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "user@example.com"
    assert data["data"]["full_name"] == "Alice Smith"

def test_update_profile_success(client, mock_db, test_user, auth_header):
    headers, _ = auth_header
    mock_db.query().filter().first.return_value = test_user

    response = client.put("/api/v1/users/me", json={"full_name": "Alice Cooper"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["full_name"] == "Alice Cooper"

def test_get_settings_success(client, mock_db, test_user, test_settings, auth_header):
    headers, _ = auth_header
    # We mock query sequentially: first for User dependency, second for settings lookup
    mock_db.query().filter().first.side_effect = [test_user, test_settings]

    response = client.get("/api/v1/users/me/settings", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["theme"] == "light"
    assert data["data"]["timezone"] == "UTC"

def test_update_settings_success(client, mock_db, test_user, test_settings, auth_header):
    headers, _ = auth_header
    mock_db.query().filter().first.side_effect = [test_user, test_settings]

    response = client.put("/api/v1/users/me/settings", json={"theme": "dark", "push_notifications": False}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["theme"] == "dark"
    assert data["data"]["push_notifications"] is False

def test_get_activities_success(client, mock_db, test_user, auth_header):
    headers, user_id = auth_header
    
    activity = UserActivity(
        id=uuid.uuid4(),
        user_id=user_id,
        action=UserActivityType.LOGIN.value,
        metadata_json={"ip": "127.0.0.1"},
        created_at=datetime.now(timezone.utc)
    )
    
    # Mock user query first, then activities query
    mock_db.query().filter().first.return_value = test_user
    mock_db.query().filter().order_by().offset().limit().all.return_value = [activity]

    response = client.get("/api/v1/users/me/activities", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["action"] == "LOGIN"
    assert data["data"][0]["metadata"]["ip"] == "127.0.0.1"
