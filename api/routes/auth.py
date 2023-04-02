from flask import Blueprint, request, abort
from controllers.users import UsersController
from config import Config
from utils.logger import log
from utils.exceptions import NotAuthorized

auth_routes = Blueprint("auth", __name__)


@auth_routes.post("/login")
def login():
    body = request.json or {}
    try:
        users = UsersController()
        email = body.get("email", "")
        password = body.get("password", "")
        if not email and not password:
            raise NotAuthorized("Bad login")
        res = users.login(email, password)
        return res.dict(
            include={"access_token": True, "user": Config.user_fields_allowlist}
        )
    except NotAuthorized as e:
        log.error(str(e))
        abort(e.status_code)
    except Exception as e:
        log.error(f"Error during login: {str(e)}")
        abort(401)
