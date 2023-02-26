from utils.db import get_db_client
from pydantic import BaseModel, Field
from controllers.decks import  make_id
import time

db = get_db_client()


class Card(BaseModel):
    id: str = Field(default_factory=make_id)
    user_id: str
    deck_id: str
    front_text: str = Field(min_length=3, max_length=128)
    back_text: str = Field(min_length=1, max_length=256)
    image_url: str | None = None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class CardUpdate(BaseModel):
    front_text: str | None = Field(min_length=3, max_length=128)
    back_text: str | None = Field(min_length=1, max_length=256)
    image_url: str | None = None
    updated_at: float = Field(default_factory=time.time)


class CardQuery(BaseModel):
    user_id: str | None = None
    deck_id: str | None = None


class CardsController:
    def create(self, card: Card) -> Card:
        card_to_dict = card.dict()
        db.cards.insert_one(card_to_dict)
        created = db.cards.find_one({"id": card.id})
        return Card.parse_obj(created)

    def update(self, card_id, payload: CardUpdate) -> Card:
        for_db = payload.dict(exclude_none=True)
        db.cards.update_one({"id": card_id}, {"$set": for_db})
        found_by_id = db.cards.find_one({"id": card_id})
        return Card.parse_obj(found_by_id)

    def delete(self, card_id) -> None:
        db.cards.delete_one({"id": card_id})

    def delete_by_deck_id(self,deck_id)-> None:
        db.cards.delete_many({"deck_id": deck_id})

    def find(self, query:CardQuery) -> list[Card]:
        q = query.dict(exclude_unset=True)
        cards_by_folder = db.cards.find(q)
        out = []
        for item in cards_by_folder:
            out.append(Card.parse_obj(item))
        return out

    def get(self, card_id: str) -> Card:
        found_by_id = db.cards.find_one({"id": card_id})
        if not found_by_id:
            raise Exception("card not found")
        return Card.parse_obj(found_by_id)


if __name__ == "__main__":
    cards = CardsController()

