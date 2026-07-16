import pytest
from unittest.mock import MagicMock
from app.modules.users.models import User
from app.modules.auth.models import RefreshToken
from app.shared.security import get_password_hash, create_access_token, create_refresh_token
import uuid
from datetime import datetime, timezone, timedelta

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

def test_register_success(client, mock_db):
    # Mock query to return None (email not registered yet)
    mock_db.query().filter().first.return_value = None
    
    response = client.post("/api/v1/auth/register", json={
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "password": "securepassword"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "jane@example.com"
    assert data["data"]["full_name"] == "Jane Doe"

def test_register_duplicate_email(client, mock_db, test_user):
    # Mock query to return an existing user
    mock_db.query().filter().first.return_value = test_user
    
    response = client.post("/api/v1/auth/register", json={
        "full_name": "John Doe",
        "email": "john@example.com",
        "password": "securepassword"
    })
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert "Email already registered" in data["message"]

def test_login_success(client, mock_db, test_user):
    # Mock query to find the user
    mock_db.query().filter().first.return_value = test_user
    
    response = client.post("/api/v1/auth/login", json={
        "email": "john@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["user"]["email"] == "john@example.com"

def test_login_invalid_password(client, mock_db, test_user):
    mock_db.query().filter().first.return_value = test_user
    
    response = client.post("/api/v1/auth/login", json={
        "email": "john@example.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "Invalid email or password" in data["message"]

def test_profile_unauthenticated(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False

def test_profile_success(client, mock_db, test_user):
    # Generate a valid access token
    token_data = {"sub": str(test_user.id), "email": test_user.email, "role": test_user.role}
    access_token = create_access_token(token_data)
    
    # Mock query to return test_user
    mock_db.query().filter().first.return_value = test_user
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "john@example.com"
