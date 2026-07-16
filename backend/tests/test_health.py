from unittest.mock import MagicMock

def test_health_check_healthy(client, mock_db):
    # Mock db.execute to run successfully
    mock_db.execute.return_value = MagicMock()
    
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "online"
    assert data["data"]["database"] == "healthy"

def test_health_check_unhealthy(client, mock_db):
    # Mock db.execute to raise an exception
    mock_db.execute.side_effect = Exception("Connection refused")
    
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["data"]["database"].startswith("unhealthy")
