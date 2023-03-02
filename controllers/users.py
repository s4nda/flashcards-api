from utils.db import get_db_client
from pydantic import BaseModel, Field, validator
import uuid
import time
import jwt
from config import Config
from argon2 import PasswordHasher

db = get_db_client()
ph = PasswordHasher()


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    password: str = Field(min_length=6, max_length=256)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    deleted_at: float | None
    reset_password_token: str | None

    @validator("email")
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError("not a valid email adress")
        return value.lower()

    @validator("password")
    def validate_password(cls, value):
        hashed = ph.hash(value)
        return hashed


class UserUpdate(BaseModel):
    name: str | None = None
    updated_at: float = Field(default_factory=time.time)


class UserLogin(BaseModel):
    access_token: str
    user: User


class UsersController:
    def create(self, user: User) -> User:
        found_user_by_email = db.users.find_one({"email": user.email})
        if found_user_by_email:
            raise Exception("user already exists")
        user_dict = user.dict()
        db.users.insert_one(user_dict)
        created_user = db.users.find_one({"id": user.id})
        return User.parse_obj(created_user)

    def update(self, user_id, payload: UserUpdate) -> User:
        to_db = payload.dict(exclude_none=True)
        db.users.update_one({"id": user_id}, {"$set": to_db})
        found = db.users.find_one({"id": user_id})
        return User.parse_obj(found)

    def delete(self, user_id) -> None:
        db.users.delete_one({"id": user_id})

    def get(self, user_id) -> User:
        found_by_id = db.users.find_one({"id": user_id})
        if not found_by_id:
            raise Exception("user not found")
        return User.parse_obj(found_by_id)

    def make_access_token(self, user: User) -> str:
        expires_at = time.time() + Config.jwt_expires_after_seconds  # 24h
        access_token = jwt.encode(
            ({"id": user.id, "email": user.email, "exp": expires_at}),
            Config.jwt_secret_key,
        )
        return access_token

    def login(self, email, password) -> UserLogin:
        found = db.users.find_one({"email": email})
        if not found:
            raise Exception("bad login")
        hashed = found.get("password", "")
        ph.verify(hashed, password)  # Verify the password
        user = User.parse_obj(found)
        return UserLogin.parse_obj(
            {"user": user, "access_token": self.make_access_token(user)}
        )

    def request_password_reset(self, email):
        found = db.users.find_one({"email": email})
        if not found:
            raise Exception("user does not exist")
        uid = str(uuid.uuid4())[:8].upper()
        db.users.update_one({"email": email}, {"$set": {"reset_password_token": uid}})
        return found["reset_password_token"]

    def reset_password(self, email, token, new_password):
        found = db.users.find_one({"reset_password_token": token})
        if not found:
            raise Exception("invalid token")
        if found and found.get("email") == email:
            db.users.update_one(
                {"email": email},
                {
                    "$set": {
                        "reset_password_token": None,
                        "password": new_password,
                        "updated_at": time.time,
                    }
                },
            )
            updated = db.users.find_one({"id": found["id"]})
        return User.parse_obj(updated)  # type: ignore
