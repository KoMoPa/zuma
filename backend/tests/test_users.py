import pytest
from fastapi.testclient import TestClient
from backend.main import app


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
    assert "email" in data
    assert "uid" in data

def test_register_user_missing_field():
    payload = {
        "email": "test@example.com"
        # no password
    }

    response = client.post("/api/users/register", json=payload)

    # Expect 400 Bad Request from API for missing field
    assert response.status_code == 400
