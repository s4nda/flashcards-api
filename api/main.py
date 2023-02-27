from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from flask import Flask, request, abort
from utils.db import get_db_client
from middleware.require_auth import require_auth
from controllers.users import UsersController, User, UserUpdate
from controllers.decks import DecksController, Deck, DeckUpdate, DeckQuery
from controllers.cards import CardsController, Card, CardUpdate, CardQuery
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = get_db_client()


@app.get("/")  # defines route, so this will be run only on localhost:8080/
def healthcheck():
    return {"version": "1.0.0"}


@app.post("/login")
def login():
    body = request.json or {}
    try:
        users = UsersController()
        email = body.get("email", "")
        password = body.get("password", "")
        res = users.login(email, password)
        return res.dict(
            include={"access_token": True, "user": Config.user_fields_allowlist}
        )
    except Exception as e:
        print("Error during /login", e)
        abort(401)


@app.post("/users")
def create_user_route():
    body = request.json or {}
    try:
        users = UsersController()
        res = users.create(User.parse_obj(body))
        return res.dict(include=Config.user_fields_allowlist)
    except Exception as e:
        print("Error during creating a user", e)
        abort(401)


@app.post("/decks")
@require_auth
def create_deck_route(user):
    body = request.json or {}
    try:
        decks = DecksController()
        body["user_id"] = user.id
        res = decks.create(Deck.parse_obj(body))
        return res.dict()
    except Exception as e:
        print("Error during creating a deck", e)
        abort(401)


@app.delete("/decks/<deck_id>/")
@require_auth
def delete_deck(user, deck_id):
    try:
        decks = DecksController()
        cards = CardsController()
        found_deck = decks.get(deck_id)
        if found_deck.user_id != user.id:
            raise Exception("User id does not match")
        decks.delete(deck_id)
        cards.delete_by_deck_id(deck_id)
        return {"success": True}
    except Exception as e:
        print("Error while deleting deck", e)
        abort(401)


@app.post("/cards")
@require_auth
def create_deck_card(user):
    body = request.json or {}
    try:
        cards = CardsController()
        body["user_id"] = user.id
        res = cards.create(Card.parse_obj(body))
        return res.dict()
    except Exception as e:
        print("Error during creating a card", e)
        abort(401)


@app.delete("/cards/<card_id>")
@require_auth
def delete_card(user, card_id):
    try:
        cards = CardsController()
        found_card = cards.get(card_id)
        if found_card.user_id != user.id:
            raise Exception("User id does not match")
        cards.delete(card_id)
        return {"success": True}
    except Exception as e:
        print("Error while deleting card", e)
        abort(401)


@app.patch("/users/<user_id>")
@require_auth
def update_user(user, user_id):
    body = request.json or {}
    try:
        users = UsersController()
        res = users.update(user.id, UserUpdate.parse_obj(body))
        return res.dict(include=Config.user_fields_allowlist)
    except Exception as e:
        print("Error", e)
        abort(401)


@app.patch("/decks/<deck_id>")
@require_auth
def update_deck(user, deck_id):
    body = request.json or {}
    try:
        decks = DecksController()
        # TODO: get deck and check if user.id matches with deck.user_id
        found_deck = decks.get(deck_id)
        if found_deck.user_id != user.id:
            raise Exception("User id does not match")
        res = decks.update(deck_id, DeckUpdate.parse_obj(body))
        return res.dict()
    except Exception as e:
        print("Error", e)
        abort(401)


@app.patch("/cards/<card_id>")
@require_auth
def update_card(user, card_id):
    body = request.json or {}
    try:
        cards = CardsController()
        found_card = cards.get(card_id)
        if found_card.user_id != user.id:
            raise Exception("User id does not match")
        res = cards.update(card_id, CardUpdate.parse_obj(body))
        return res.dict()
    except Exception as e:
        print("Error", e)
        abort(401)


@app.get("/decks")
@require_auth
def get_user_decks(user: User):
    try:
        decks = DecksController()
        query = {"user_id": user.id}
        res = decks.find(DeckQuery(**query))
        return [deck.dict() for deck in res]
    except Exception as e:
        print("Error: Not Found", e)
        abort(404)


@app.get("/decks/<deck_id>")
@require_auth
def get_deck_by_id(user: User, deck_id: str):
    try:
        decks = DecksController()
        found_deck = decks.get(deck_id)
        if found_deck.user_id != user.id:
            raise Exception("User id does not match")
        return found_deck.dict()
    except Exception as e:
        print("Error: Not Found")
        abort(404)


@app.get("/decks/<deck_id>/cards")
@require_auth
def get_all_deck_cards(user: User, deck_id: str):
    try:
        cards = CardsController()
        query = {"user_id": user.id, "deck_id": deck_id}
        found_cards = cards.find(CardQuery.parse_obj(query))
        return [card.dict() for card in found_cards]
    except Exception as e:
        print("Error, Not Found", e)
        abort(404)


@app.get("/decks/<deck_id>/cards/<card_id>")
@require_auth
def get_private_deck_card(user, deck_id, card_id):
    try:
        cards = CardsController()
        found_card = cards.get(card_id)
        if found_card.user_id != user.id:
            raise Exception("Error, not allowed")
        return found_card.dict()
    except Exception as e:
        print("Error: Not Found")
        abort(404)


"""
Public routes below (no auth)
"""


@app.get("/public/decks")
def get_public_decks():
    try:
        decks = DecksController()
        query = {"public": True}
        res = decks.find(DeckQuery(**query))
        return [deck.dict() for deck in res]
    except Exception as e:
        print("Error: Not Found", e)
        abort(404)


@app.get("/public/decks/<deck_id>")
def get_public_deck(deck_id):
    decks = DecksController()
    deck = decks.get(deck_id)
    if not deck.public:
        raise Exception("Error: Not Found")
    else:
        return deck.dict()


@app.get("/public/decks/<deck_id>/cards")
def get_deck_cards(deck_id):
    try:
        cards = CardsController()
        query = {"deck_id": deck_id}
        res = cards.find(CardQuery(**query))
        return [card.dict() for card in res]
    except Exception as e:
        print("Error: Not Found", e)
        abort(404)


@app.get("/public/decks/<deck_id>/cards/<card_id>")
def get_deck_card(deck_id, card_id):
    try:
        cards = CardsController()
        res = cards.get(card_id)
        return res.dict()
    except Exception as e:
        print("Error: Not Found", e)
        abort(404)
