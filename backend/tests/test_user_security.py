import pytest
from unittest.mock import MagicMock
import uuid
from datetime import datetime, timezone
from app.modules.users.models.user import User
from app.modules.auth.models import RefreshToken
from app.shared.security import create_access_token, get_password_hash, verify_password

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
        password_hash=get_password_hash("oldpassword123"),
        avatar_url=None,
        role="USER",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

def test_change_password_wrong_current(client, mock_db, test_user, auth_header):
    headers, _ = auth_header
    mock_db.query().filter().first.return_value = test_user

    response = client.put("/api/v1/users/me/password", json={
        "old_password": "wrongpassword",
        "new_password": "newpassword123"
    }, headers=headers)
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "Incorrect current password" in data["message"]

def test_change_password_success(client, mock_db, test_user, auth_header):
    headers, user_id = auth_header
    mock_db.query().filter().first.return_value = test_user

    # Mock delete for refresh tokens
    delete_mock = MagicMock()
    mock_db.query().filter().delete = delete_mock

    response = client.put("/api/v1/users/me/password", json={
        "old_password": "oldpassword123",
        "new_password": "newpassword123"
    }, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Password changed successfully" in data["message"]
    
    # Confirm password hash updated
    assert verify_password("newpassword123", test_user.password_hash)
    
    # Verify that revoke/delete was called for RefreshTokens
    assert delete_mock.called
