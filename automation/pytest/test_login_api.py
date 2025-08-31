import requests

BASE_URL = "https://example.com/api/v1/auth"  # replace with your API base URL
VALID_EMAIL = "user@example.com"
VALID_PASSWORD = "Passw0rd!"
INVALID_PASSWORD = "WrongPassword"


def test_login_valid_credentials():
    response = requests.post(f"{BASE_URL}/login", json={
        "email": VALID_EMAIL,
        "password": VALID_PASSWORD
    })
    assert response.status_code == 200
    data = response.json()
    assert "token" in data or "access_token" in data


def test_login_invalid_password():
    response = requests.post(f"{BASE_URL}/login", json={
        "email": VALID_EMAIL,
        "password": INVALID_PASSWORD
    })
    assert response.status_code in [400, 401]
    data = response.json()
    assert "error" in data or "message" in data


def test_login_empty_fields():
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "",
        "password": ""
    })
    assert response.status_code in [400, 422]
    data = response.json()
    assert "error" in data or "message" in data
