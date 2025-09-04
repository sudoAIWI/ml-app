import pytest
from fastapi.testclient import TestClient
from app import app
from training import train_model, save_model
import os


# Train model for tests
@pytest.fixture(scope="session", autouse=True)
def setup_model():
    """Train and save model before running tests"""
    if not os.path.exists("model.joblib"):
        model, target_names = train_model()
        save_model(model, target_names, "test_model.joblib")


client = TestClient(app)


def test_predict_endpoint():
    """Test prediction endpoint with valid data"""
    test_data = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "probabilities" in response.json()


def test_predict_invalid_data():
    """Test prediction endpoint with invalid data"""
    test_data = {
        "sepal_length": "invalid",  # Wrong type
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    response = client.post("/predict", json=test_data)
    assert response.status_code == 422  # Validation error
