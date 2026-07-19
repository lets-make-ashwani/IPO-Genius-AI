import pytest
from unittest.mock import MagicMock, patch
from app.modules.users.models import User
from app.shared.security import get_password_hash, create_password_reset_token
import uuid
from datetime import datetime, timezone

@pytest.fixture
def test_user():
    return User(
        id=uuid.uuid4(),
        full_name="John Doe",
        email="john@example.com",
        password_hash=get_password_hash("password123"),
        role="USER",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

def test_forgot_password_generic_response(client, mock_db, test_user):
    # Case 1: User exists
    mock_db.query().filter().first.return_value = test_user
    
    with patch("app.shared.email_provider.email_provider.send_email") as mock_send:
        response = client.post("/api/v1/auth/forgot-password", json={"email": "john@example.com"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "If the email exists" in data["message"]
        mock_send.assert_called_once()

    # Case 2: User does not exist (same generic response)
    mock_db.query().filter().first.return_value = None
    with patch("app.shared.email_provider.email_provider.send_email") as mock_send:
        response = client.post("/api/v1/auth/forgot-password", json={"email": "unknown@example.com"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "If the email exists" in data["message"]
        mock_send.assert_not_called()


def test_reset_password_success(client, mock_db, test_user):
    mock_db.query().filter().first.return_value = test_user
    
    token = create_password_reset_token(test_user.email)
    
    response = client.post("/api/v1/auth/reset-password", json={
        "token": token,
        "new_password": "newpassword123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "reset successfully" in data["message"]


def test_reset_password_invalid_token(client, mock_db):
    response = client.post("/api/v1/auth/reset-password", json={
        "token": "invalid_or_malformed_token_string",
        "new_password": "newpassword123"
    })
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "Invalid or expired password reset link" in data["message"]


def test_forgot_password_rate_limiting(client, mock_db, test_user):
    mock_db.query().filter().first.return_value = test_user
    
    # Reset history of the limiter for clean run
    from app.shared.rate_limiter import forgot_password_limiter
    forgot_password_limiter.history.clear()
    
    # Perform 5 requests (which is the limit)
    for _ in range(5):
        res = client.post("/api/v1/auth/forgot-password", json={"email": "john@example.com"})
        assert res.status_code == 200

    # The 6th request should be rate-limited with HTTP 429
    res = client.post("/api/v1/auth/forgot-password", json={"email": "john@example.com"})
    assert res.status_code == 429
    data = res.json()
    assert data["success"] is False
    assert "Too many password reset attempts" in data["message"]
