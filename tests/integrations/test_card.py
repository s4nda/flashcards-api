import requests
from tests.utils.utils import login_and_create_user

api_url = "http://localhost:8080"


def test_create_card():
    logged_in_user = login_and_create_user(email="createcard@test.com")
    token = logged_in_user["access_token"]
    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "Test", "description": "TEST"},
        headers={"Authorization": f"Bearer {token}"},
    )
    r_deck.raise_for_status()
    created_deck = r_deck.json()

    r_card = requests.post(
        f"{api_url}/cards",
        json={
            "deck_id": created_deck["id"],
            "front_text": "question?",
            "back_text": "answer",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    r_card.raise_for_status()
    created_card = r_card.json()
    assert created_card
    assert created_card["deck_id"] == created_deck["id"]
    assert created_card["user_id"] == logged_in_user["user"]["id"]


def test_update_card():
    logged_in_user = login_and_create_user(email="updatecard@test.com")
    token = logged_in_user["access_token"]
    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "Title", "description": "Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    r_deck.raise_for_status()
    created_deck = r_deck.json()

    r_card = requests.post(
        f"{api_url}/cards",
        json={
            "deck_id": created_deck["id"],
            "front_text": "Question?",
            "back_text": "Answer",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    r_card.raise_for_status()
    created_card = r_card.json()
    card_id = created_card["id"]

    r_updated = requests.patch(
        f"{api_url}/cards/{card_id}",
        json={
            "front_text": "Who painted the Mona Lisa?",
            "back_text": "Leonardo Da Vinci",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    r_updated.raise_for_status()
    updated = r_updated.json()
    assert updated["front_text"] == "Who painted the Mona Lisa?"
    assert updated["back_text"] == "Leonardo Da Vinci"


def test_delete_card():
    logged_in_user = login_and_create_user(email="deletecard@test.com")
    token = logged_in_user["access_token"]

    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "Title", "description": "Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    r_deck.raise_for_status()
    created_deck = r_deck.json()

    r_card = requests.post(
        f"{api_url}/cards",
        json={
            "deck_id": created_deck["id"],
            "front_text": "Question?",
            "back_text": "Answer",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    r_card.raise_for_status()
    created_card = r_card.json()
    card_id = created_card["id"]
    r_delete = requests.delete(
        f"{api_url}/cards/{card_id}", headers={"Authorization": f"Bearer {token}"}
    )
    r_delete.raise_for_status()
    deleted = r_delete.json()
    assert deleted


def test_delete_card_wrong_user():
    user_a = login_and_create_user(email="delete_card_user_a@test.com")
    token_a = user_a["access_token"]
    user_b = login_and_create_user(email="delete_card_user_b@test.com")
    token_b = user_b["access_token"]

    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "Title", "description": "Description"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    r_deck.raise_for_status()
    created_deck = r_deck.json()

    r_card = requests.post(
        f"{api_url}/cards",
        json={
            "deck_id": created_deck["id"],
            "front_text": "Question?",
            "back_text": "Answer",
        },
        headers={"Authorization": f"Bearer {token_a}"},
    )
    r_card.raise_for_status()
    created_card = r_card.json()
    card_id = created_card["id"]

    r_delete = requests.delete(
        f"{api_url}/cards/{card_id}", headers={"Authorization": f"Bearer {token_b}"}
    )

    assert r_delete.status_code == 401


def test_update_card_wrong_user():
    user_a = login_and_create_user(email="update_card_user_a@test.com")
    token_a = user_a["access_token"]
    user_b = login_and_create_user(email="update_card_user_b@test.com")
    token_b = user_b["access_token"]

    r_deck = requests.post(
        f"{api_url}/decks",
        json={"name": "Title", "description": "Description"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    r_deck.raise_for_status()
    created_deck = r_deck.json()

    r_card = requests.post(
        f"{api_url}/cards",
        json={
            "deck_id": created_deck["id"],
            "front_text": "Question?",
            "back_text": "Answer",
        },
        headers={"Authorization": f"Bearer {token_a}"},
    )
    r_card.raise_for_status()
    created_card = r_card.json()
    card_id = created_card["id"]

    r_updated = requests.patch(
        f"{api_url}/cards/{card_id}",
        json={
            "front_text": "Who painted the Mona Lisa?",
            "back_text": "Leonardo Da Vinci",
        },
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert r_updated.status_code == 401
