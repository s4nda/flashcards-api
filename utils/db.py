from pymongo import MongoClient
from config import Config
import certifi


def get_db_client():
    client = MongoClient(Config.mongodb_uri, tlsCAFile=certifi.where())
    selected_db = client[Config.mongodb_db_name]
    return selected_db
