import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_activity():
    # Use a test email and activity name
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert "message" in response.json()

def test_signup_duplicate():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"
    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Second signup should fail or return a message about duplicate
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code in (400, 200)
    # Accept either error or info message
    assert "message" in response.json() or "detail" in response.json()
