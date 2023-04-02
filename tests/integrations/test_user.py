from utils.db import get_db_client
from tests.utils.utils import create_test_user, login_and_create_user
import requests

api_url = "http://localhost:8080"
db = get_db_client()


def test_create_user():
    user = create_test_user(email="dennisreynolds@test.com")
    assert user["email"] == "dennisreynolds@test.com"
    assert user["name"] == "Test User"


def test_create_user_bad_email():
    r_user = requests.post(
        f"{api_url}/users",
        json={"email": "bademail.com", "password": "password123", "name": "Test User"},
    )
    assert r_user.status_code == 400


def test_user_password_not_visible():
    logged_in_user = login_and_create_user("canyouseemypassword@test.com")
    token = logged_in_user["access_token"]

    get_user = requests.get(
        f"{api_url}/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert get_user.status_code == 200
    found_user = get_user.json()
    assert found_user.get("password") == None
