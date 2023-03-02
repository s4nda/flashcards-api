from config import Config
from utils.db import get_db_client

Config.mongodb_db_name = "flashcards-test"  # Hardcoded db name
# Santity check -- allow tests to run only on -test database
if not Config.mongodb_db_name.endswith("-test"):
    raise ValueError("Aborting tests, database for tests needs to ends with -test")

# Prepare clean DB for testing
db = get_db_client()
for collection in db.list_collection_names():
    db.drop_collection(collection)

# Seed
#seed_data()
