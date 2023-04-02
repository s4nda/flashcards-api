from functools import wraps
import jwt
from flask import request
from config import Config
from controllers.users import UsersController


def optional_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        current_user = None
        try:
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if token:
                decoded = jwt.decode(token, Config.jwt_secret_key, algorithms=["HS256"])
                users = UsersController()
                current_user = users.get(decoded["id"])
            # NOTE: Deliberately disabling error, user may be logged in or None
            # if current_user is None:
            #     return {
            #         "message": "Invalid Authentication token!",
            #         "data": None,
            #         "error": "Unauthorized",
            #     }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "error": str(e),
            }, 500
        return f(current_user, *args, **kwargs)

    return decorated
