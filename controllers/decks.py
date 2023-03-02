from utils.db import get_db_client
from typing import List
from pydantic import BaseModel, Field, validator
import uuid
import time

db = get_db_client()


def make_id():
    return str(uuid.uuid4())


class Deck(BaseModel):
    id: str = Field(default_factory=make_id)
    user_id: str
    name: str = Field(min_length=3, max_length=64)
    description: str | None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    tags: List["str"] | None = []
    public: bool = False

    @validator("tags", each_item=True)
    def tags_alphanumeric(cls, value):
        value = value.lower()
        if not value.isalnum():
            raise ValueError("tags must be alphanumeric")
        return value


class DeckUpdate(BaseModel):
    name: str | None = Field(min_length=3, max_length=64)
    description: str | None
    public: bool | None
    updated_at: float = Field(default_factory=time.time)


class DeckQuery(BaseModel):
    user_id: str | None = None
    public: bool | None = None
    tags: List["str"] | None = []


class DecksController:
    def create(self, deck: Deck) -> Deck:
        deck_to_dict = deck.dict()
        db.decks.insert_one(deck_to_dict)
        created_deck = db.decks.find_one({"id": deck.id})
        return Deck.parse_obj(created_deck)

    def update(self, deck_id: str, payload: DeckUpdate) -> Deck:
        for_db = payload.dict(exclude_none=True)
        db.decks.update_one({"id": deck_id}, {"$set": for_db})
        found_by_id = db.decks.find_one({"id": deck_id})
        return Deck.parse_obj(found_by_id)

    def delete(self, deck_id: str) -> None:
        db.decks.delete_one({"id": deck_id})

    def get(self, deck_id: str) -> Deck:
        found_by_id = db.decks.find_one({"id": deck_id})
        if not found_by_id:
            raise Exception("deck not found")
        return Deck.parse_obj(found_by_id)

    def find(self, query: DeckQuery) -> list[Deck]:
        q = query.dict(exclude_unset=True)
        decks_find = db.decks.find(q)
        out = []
        for item in decks_find:
            out.append(Deck.parse_obj(item))
        return out





