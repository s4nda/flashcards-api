from flask import Blueprint, request, abort
from controllers.cards import CardsController, CardQuery, CardUpdate, Card
from controllers.users import User
from middleware.require_auth import require_auth
from middleware.optional_auth import optional_auth
from utils.logger import log
from utils.exceptions import NotAuthorized, ResourceNotFound

card_routes = Blueprint("card", __name__)


# create card
@card_routes.post("/cards")
@require_auth
def create_card(user: User):
    body = request.json or {}
    try:
        cards = CardsController()
        body["user_id"] = user.id
        res = cards.create(Card.parse_obj(body))
        return res.dict()
    except Exception as e:
        log.error(f"Error during creating card: {str(e)}")
        abort(500)


# update card
@card_routes.patch("/cards/<card_id>")
@require_auth
def update_card(user, card_id):
    body = request.json or {}
    try:
        cards = CardsController()
        found_card = cards.get(card_id)
        if found_card.user_id != user.id:
            raise NotAuthorized("Not Owner")
        res = cards.update(card_id, CardUpdate.parse_obj(body))
        return res.dict()
    except NotAuthorized as e:
        abort(e.status_code)
    except ResourceNotFound as e:
        abort(e.status_code)
    except Exception as e:
        log.error(f"Error updating card: {str(e)}")
        abort(500)


# delete card
@card_routes.delete("/cards/<card_id>")
@require_auth
def delete_card(user, card_id):
    try:
        cards = CardsController()
        found_card = cards.get(card_id)
        if found_card.user_id != user.id:
            raise NotAuthorized("Not Owner")
        cards.delete(card_id)
        return "", 204  # 204 No content
    except NotAuthorized as e:
        abort(e.status_code)
    except ResourceNotFound as e:
        abort(e.status_code)
    except Exception as e:
        log.error(f"Error while deleting card: {str(e)}")
        abort(500)


# get cards
@card_routes.get("/cards")
@optional_auth
def get_cards(user: User):
    try:
        cards = CardsController()
        limit = request.args.get("limit", default=20, type=int)
        offset = request.args.get("offset", default=0, type=int)
        deck_id = request.args.get("deck_id", type=str)
        user_id = request.args.get("user_id", type=str)
        query = CardQuery()
        query.deck_id = deck_id
        if deck_id:
            query.deck_id = deck_id
        if user_id:
            query.user_id = user_id
        found_cards = cards.find(query, limit=limit, offset=offset)
        return [card.dict() for card in found_cards]
    except Exception as e:
        log.error(f"Error, Not Found: {str(e)}")
        abort(500)


# get card by id
@card_routes.get("/cards/<card_id>")
@optional_auth
def get_card(user, card_id):
    try:
        cards = CardsController()
        found_card = cards.get(card_id)
        if user and user.id != found_card.user_id:
            raise NotAuthorized("Not Owner")
        return found_card.dict()
    except NotAuthorized as e:
        abort(e.status_code)
    except ResourceNotFound as e:
        abort(e.status_code)
    except Exception as e:
        log.error(f"Error, Not Found: {str(e)}")
        abort(500)
