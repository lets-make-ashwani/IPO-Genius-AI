import pytest
from unittest.mock import MagicMock, patch
import uuid
import io
from datetime import datetime, timezone
from app.modules.users.models.user import User
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

def test_upload_avatar_invalid_extension(client, mock_db, test_user, auth_header):
    headers, _ = auth_header
    mock_db.query().filter().first.return_value = test_user

    response = client.post(
        "/api/v1/users/me/avatar",
        files={"file": ("invalid.txt", b"some text", "text/plain")},
        headers=headers
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "Invalid file type" in data["message"]

def test_upload_avatar_too_large(client, mock_db, test_user, auth_header):
    headers, _ = auth_header
    mock_db.query().filter().first.return_value = test_user

    # Create dummy bytes larger than 5 MB
    large_bytes = b"0" * (5 * 1024 * 1024 + 1)
    
    response = client.post(
        "/api/v1/users/me/avatar",
        files={"file": ("avatar.png", large_bytes, "image/png")},
        headers=headers
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "File size exceeds 5 MB" in data["message"]

@patch("app.modules.users.services.storage.Image.open")
def test_upload_avatar_success(mock_image_open, client, mock_db, test_user, auth_header):
    headers, _ = auth_header
    mock_db.query().filter().first.return_value = test_user

    # Mock PIL image behavior
    mock_img = MagicMock()
    mock_img.mode = "RGBA"
    mock_img.convert.return_value = mock_img
    mock_image_open.return_value = mock_img

    with patch("builtins.open", MagicMock()):
        with patch("os.makedirs", MagicMock()):
            response = client.post(
                "/api/v1/users/me/avatar",
                files={"file": ("avatar.png", b"fake image bytes", "image/png")},
                headers=headers
            )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["avatar_url"] is not None
    assert "/static/avatars/" in data["data"]["avatar_url"]
