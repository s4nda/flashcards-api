import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class Config:
    # JWT Config
    jwt_secret_key = os.getenv("JWT_SECRET_KEY", "")
    jwt_expires_after_seconds = 60 * 60 * 24  # 24h
    # Database config
    mongodb_uri = os.getenv("MONGODB_URI")
    mongodb_db_name = os.getenv("MONGODB_DB_NAME", "")
    # user config
    user_fields_allowlist = {"created_at", "updated_at", "name", "email", "id"}
    # Log level
    log_level = int(os.getenv("LOG_LEVEL", "40"))
