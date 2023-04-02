from flask import Blueprint, request, abort
from controllers.users import UsersController, User, UserUpdate
from middleware.require_auth import require_auth
from config import Config
from utils.logger import log
from utils.exceptions import ResourceNotFound


user_routes = Blueprint("user", __name__)


# create user
@user_routes.post("/users")
def create_user():
    body = request.json or {}
    try:
        users = UsersController()
        res = users.create(User.parse_obj(body))
        return res.dict(include=Config.user_fields_allowlist)
    except Exception as e:
        log.error(f"Error during creating a user: {str(e)}")
        return abort(500)


# update user
@user_routes.patch("/me")
@require_auth
def update_user(user):
    body = request.json or {}
    try:
        users = UsersController()
        user_to_update = users.get(user.id)
        res = users.update(user_to_update.id, UserUpdate.parse_obj(body))
        return res.dict(include=Config.user_fields_allowlist)
    except ResourceNotFound as e:
        abort(e.status_code)
    except Exception as e:
        log.error(f"Error updating a user: {str(e)}")
        abort(500)


@user_routes.get("/me")
@require_auth
def get_logged_in_user(user: User):
    try:
        users = UsersController()
        found_user = users.get(user.id)
        return found_user.dict(include=Config.user_fields_allowlist)
    except ResourceNotFound as e:
        abort(e.status_code)
    except Exception as e:
        log.error(f"Error returning a user: {str(e)}")
        abort(401)
