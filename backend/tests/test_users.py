
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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


# Test updating a user
def test_update_user_success():
    # First, register a user
    payload = {
        "email": "updateuser@example.com",
        "password": "password123"
    }
    reg_response = client.post("/api/users/register", json=payload)
    assert reg_response.status_code in (200, 201)
    uid = reg_response.json()["uid"]

    # Now, update the user's display name
    update_payload = {"display_name": "Updated User"}
    update_response = client.put(f"/api/users/update/{uid}", json=update_payload)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["uid"] == uid
    assert data["display_name"] == "Updated User"


# Test deleting a user
def test_delete_user_success():
    # First, register a user
    payload = {
        "email": "deleteuser@example.com",
        "password": "password123"
    }
    reg_response = client.post("/api/users/register", json=payload)
    assert reg_response.status_code in (200, 201)
    uid = reg_response.json()["uid"]

    # Now, delete the user
    delete_response = client.delete(f"/api/users/delete/{uid}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert "message" in data
    assert str(uid) in data["message"]
