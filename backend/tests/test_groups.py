
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_create_group_success():
	payload = {
		"name": "Test Group",
		"members": ["user1", "user2"]
	}
	response = client.post("/api/groups", json=payload)
	assert response.status_code == 200 or response.status_code == 201
	data = response.json()
	assert "group_id" in data
	assert data["name"] == "Test Group"
	assert data["members"] == ["user1", "user2"]
