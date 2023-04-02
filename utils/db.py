from pymongo import MongoClient
from config import Config
import certifi


def get_db_client():
    client = MongoClient(
        Config.mongodb_uri,
        connectTimeoutMS=5000,
        tlsCAFile=None
        if "localhost" in Config.mongodb_uri# type: ignore
        else certifi.where(),  # This line may create problems when using docker/local
    )
    selected_db = client[Config.mongodb_db_name]
    return selected_db
