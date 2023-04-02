from flask import Blueprint, request, abort
from controllers.users import User
from controllers.decks import DecksController, Deck, DeckUpdate, DeckQuery
from controllers.cards import CardsController
from middleware.require_auth import require_auth
from utils.logger import log
from middleware.optional_auth import optional_auth
from utils.exceptions import NotAuthorized, ResourceNotFound


deck_routes = Blueprint("deck", __name__)


# create deck
@deck_routes.post("/decks")
@require_auth
def create_deck(user):
    body = request.json or {}
    try:
        decks = DecksController()
        body["user_id"] = user.id
        res = decks.create(Deck.parse_obj(body))
        return res.dict()
    except ValueError:
        abort(400)
    except Exception as e:
        log.error(f"Error creating deck: {str(e)}")
        abort(500)


# update deck
@deck_routes.patch("/decks/<deck_id>")
@require_auth
def update_deck(user, deck_id):
    body = request.json or {}
    try:
        decks = DecksController()
        found_deck = decks.get(deck_id)
        if found_deck.user_id != user.id:
            raise NotAuthorized("Not Owner")
        res = decks.update(deck_id, DeckUpdate.parse_obj(body))
        return res.dict()
    except NotAuthorized as e:
        abort(e.status_code)
    except ResourceNotFound as e:
        abort(e.status_code)
    except Exception as e:
        log.error(f"Error updating deck: {str(e)}")
        abort(500)


# delete deck
@deck_routes.delete("/decks/<deck_id>/")
@require_auth
def delete_deck(user, deck_id):
    try:
        decks = DecksController()
        cards = CardsController()
        found_deck = decks.get(deck_id)
        if found_deck.user_id != user.id:
            raise NotAuthorized("Not Owner")
        decks.delete(deck_id)
        cards.delete_by_deck_id(deck_id)
        return "", 204  # 204 No Content
    except NotAuthorized as e:
        abort(e.status_code)
    except ResourceNotFound as e:
        abort(e.status_code)
    except Exception as e:
        log.error(f"Error deleting deck: {str(e)}")
        abort(500)


# get decks
@deck_routes.get("/decks")
@optional_auth
def get_decks(user: User):
    try:
        decks = DecksController()
        user_id = request.args.get("user_id", type=str)
        limit = request.args.get("limit", default=20, type=int)
        offset = request.args.get("offset", default=0, type=int)
        public = request.args.get("public", type=bool)
        query = DeckQuery()
        query.user_id = user_id
        if public is not None:
            query.public = public
        # Can query both public and private decks
        if not user or (user and user.id != user_id):
            query.public = True
        res = decks.find(query, limit=limit, offset=offset)
        return [deck.dict() for deck in res]
    except Exception as e:
        log.error(f"Error: Not Found: {str(e)}")
        abort(500)


# get one deck by id
@deck_routes.get("/decks/<deck_id>")
@optional_auth
def get_deck(user, deck_id):
    try:
        decks = DecksController()
        found_deck = decks.get(deck_id)
        # For "me"
        if user and user.id == found_deck.user_id:
            return found_deck.dict()
        # For public decks
        if found_deck.public:
            return found_deck.dict()
        else:
            # Deck exists but not public and user is not owner
            raise NotAuthorized("Not Owner")
    except NotAuthorized as e:
        abort(e.status_code)
    except ResourceNotFound as e:
        abort(e.status_code)
    except Exception as e:
        log.error(f"Error: Not Found{str(e)}")
        abort(404)
