from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the ML API" in response.json()["message"]


def test_health_endpoint():
    """Test health endpoint returns ok status"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
