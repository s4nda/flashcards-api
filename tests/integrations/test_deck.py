import requests
from tests.utils.utils import login_and_create_user

api_url = "http://localhost:8080"


def test_create_deck():
    logged_in_user = login_and_create_user(email="creatingdeck@test.com")
    token = logged_in_user["access_token"]
    assert token

    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "Test", "description": "TEST"},
        headers={"Authorization": f"Bearer {token}"},
    )
    r_deck.raise_for_status()
    created_deck = r_deck.json()
    assert created_deck


def test_update_deck():
    logged_in_user = login_and_create_user(email="updatedeck@test.com")
    token = logged_in_user["access_token"]

    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "test", "description": "testing"},
        headers={"Authorization": f"Bearer {token}"},
    )
    r_deck.raise_for_status()
    created_deck = r_deck.json()
    deck_id = created_deck["id"]

    r_update = requests.patch(
        f"{api_url}/decks/{deck_id}",
        json={"name": "Test Passed", "description": "upd"},
        headers={"Authorization": f"Bearer {token}"},
    )
    r_update.raise_for_status()
    updated = r_update.json()
    assert updated["name"] == "Test Passed"
    assert updated["description"] == "upd"


def test_delete_deck():
    user = login_and_create_user(email="testuser@test.com")
    token = user["access_token"]

    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "test?", "description": "TEST"},
        headers={"Authorization": f"Bearer {token}"},
    )
    r_deck.raise_for_status()
    created_deck = r_deck.json()
    deck_id = created_deck["id"]
    r_del = requests.delete(
        f"{api_url}/decks/{deck_id}", headers={"Authorization": f"Bearer {token}"}
    )
    r_del.raise_for_status()
    deleted = r_del.json()
    assert deleted


def test_create_deck_bad_token():
    login_and_create_user(email="badtoken@test.com")
    token = "DUMMYTOKEN"
    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "test", "description": "test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r_deck.status_code == 500


def test_delete_deck_wrong_user():
    user_a = login_and_create_user(email="delete_deck_user_a@test.com")
    token_a = user_a["access_token"]
    user_b = login_and_create_user(email="delete_deck_user_b@test.com")
    token_b = user_b["access_token"]
    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "test?", "description": "TEST"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    r_deck.raise_for_status()
    user_a_created_deck = r_deck.json()
    deck_id = user_a_created_deck["id"]
    r_del = requests.delete(
        f"{api_url}/decks/{deck_id}", headers={"Authorization": f"Bearer {token_b}"}
    )
    assert r_del.status_code == 401


def test_update_deck_wrong_user():
    user_a = login_and_create_user(email="update_deck_user_a@test.com")
    token_a = user_a["access_token"]
    user_b = login_and_create_user(email="update_deck_user_b@test.com")
    token_b = user_b["access_token"]
    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "test?", "description": "TEST"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    r_deck.raise_for_status()
    user_a_created_deck = r_deck.json()
    deck_id = user_a_created_deck["id"]

    r_update = requests.patch(
        f"{api_url}/decks/{deck_id}",
        json={"name": "title", "description": "text"},
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert r_update.status_code == 401
