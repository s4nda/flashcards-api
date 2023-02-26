from pymongo import MongoClient
from config import Config
import ssl


def get_db_client():
    client = MongoClient(Config.mongodb_uri, tls=True, tlsAllowInvalidCertificates=True)
    selected_db = client[Config.mongodb_db_name]
    return selected_db
