import requests
from tests.utils.utils import create_test_user, login_and_create_user


api_url = "http://localhost:8080"


def test_login_success():
    logged_in_user = login_and_create_user(email="frankraynolds@test.com")
    assert logged_in_user["user"]
    assert logged_in_user["access_token"]


def test_login_failure():
    create_test_user(email="test_login_failure@test.com")
    r_login = requests.post(
        f"{api_url}",
        json={"email": "test_login_failure@test.com", "password": "wrongpassword"},
    )
    assert r_login.status_code == 405


def test_login_not_exist_user():
    r_login = requests.post(
        f"{api_url}",
        json={
            "email": "non_existing_email@test.com",
            "password": "nonexistingpassword",
        },
    )

    assert r_login.status_code == 405
