from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_signup_success():
    # Use a unique email for each test run if database is persistent
    import uuid
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "email": email,
        "password": "password123"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == email

def test_signup_duplicate_email():
    payload = {
        "email": "existing@example.com",
        "password": "password123"
    }
    # Initial signup
    client.post("/api/auth/register", json=payload)
    # Duplicate signup
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_success():
    email = "login_test@example.com"
    password = "password123"
    # Ensure user exists
    client.post("/api/auth/register", json={
        "email": email,
        "password": password
    })
    
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = client.post("/api/auth/login", json={"email": "wrong@example.com", "password": "wrong"})
    assert response.status_code == 401
