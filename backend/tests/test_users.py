import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Example test for your /api/users/register route
def test_register_user_success():
    payload = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }

    response = client.post("/api/users/register", json=payload)

    # Check response
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "id" in data or "uid" in data  # depending on how you return user info

def test_register_user_missing_field():
    payload = {
        "email": "test@example.com"
        # no password
    }

    response = client.post("/api/users/register", json=payload)

    # Expect validation error from FastAPI
    assert response.status_code == 422
