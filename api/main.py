from flask import Flask, request
from utils.db import get_db_client
from api.routes.auth import auth_routes
from api.routes.users import user_routes
from api.routes.decks import deck_routes
from api.routes.cards import card_routes
from flask_cors import CORS
from middleware.optional_auth import optional_auth
from utils.logger import log

app = Flask(__name__)
CORS(app)
db = get_db_client()


log.info("Server running on http://localhost:8080")


@app.get("/")  # defines route, so this will be run only on localhost:8080/
def healthcheck():
    log.debug("Hit healthcheck endpoint")
    return {"version": "1.0.0"}


@app.get("/debug")
@optional_auth
def debug(user):
    if user:
        return {"ulogovan": True}
    # Grabbing query params ?user_id
    user_id = request.args.get("user_id", type=str)
    return {"ok": True, "TEST": user_id}


# Registering routes
app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)
app.register_blueprint(deck_routes)
app.register_blueprint(card_routes)




if __name__ == "__main__":
    # This server is only for local/debug
    app.run(port=8080, debug=True)
