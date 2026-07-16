import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import get_db

@pytest.fixture
def mock_db():
    db = MagicMock()
    # Mock some standard query behaviors if needed
    return db

@pytest.fixture
def client(mock_db):
    # Override get_db dependency to yield mock_db
    def override_get_db():
        try:
            yield mock_db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
