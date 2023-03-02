from utils.db import get_db_client
from tests.utils.utils import create_test_user
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
