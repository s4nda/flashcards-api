from config import Config

Config.mongodb_db_name = "flashcards-test"

from api.main import app


if __name__ == "__main__":
    app.run(port=8080)
