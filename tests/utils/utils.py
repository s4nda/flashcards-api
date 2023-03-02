import requests

api_url = "http://localhost:8080"
# use pytest tests -rP to see output


def create_test_user(
    email="test@test.com",
    name="Test User",
    password="dummypassword123",
    raise_for_status=True,
):
    r_user = requests.post(
        f"{api_url}/users",
        json={
            "email": email,
            "name": name,
            "password": password,
        },
    )
    if raise_for_status:
        r_user.raise_for_status()
    user = r_user.json()
    return user


def login_and_create_user(email="default_test_user@test.com", password="asdfasdf123"):
    create_test_user(email, password=password)
    user_login = requests.post(
        f"{api_url}/login",
        json={"email": email, "password": password},
    )
    user_login.raise_for_status()
    logged_in_user = user_login.json()
    return logged_in_user
