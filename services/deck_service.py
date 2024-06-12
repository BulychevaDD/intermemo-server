from datetime import datetime

from models.db import Deck
from repositories.deck_repository import DeckRepository


class DeckService:
    repository: DeckRepository

    def __init__(self):
        self.repository = DeckRepository()

    def create(self, name: str, description: str, owner_id: int) -> Deck:
        deck = Deck(name=name, description=description, owner_id=owner_id)

        created_deck_id = self.repository.add(deck)
        return self.repository.get_by_id(created_deck_id)

    def delete(self, deck_id: int) -> Deck:
        self.repository.delete(deck_id)

    def get_by_id(self, deck_id: int) -> Deck | None:
        return self.repository.get_by_id(deck_id)

    def get_all_by_owner(self, owner_id: int) -> list[Deck]:
        return self.repository.get_all_by_owner(owner_id)

    def update(self, deck_id: int, name: str, description: str) -> Deck | None:
        existing_deck = self.repository.get_by_id(deck_id)

        existing_deck.name = name
        existing_deck.description = description

        updated_deck_id = self.repository.update(existing_deck)
        return self.repository.get_by_id(updated_deck_id)

    def set_last_study(self, deck_id: int) -> None:
        deck = self.repository.get_by_id(deck_id)

        deck.last_study = datetime.now()
        self.repository.update(deck)
