from datetime import datetime, timedelta

from core.get_ire import get_ire
from models.db import Card
from repositories.card_repository import CardRepository


class CardService:
    repository: CardRepository

    def __init__(self):
        self.repository = CardRepository()

    def create(self, question: str, answer: str, difficulty: int, deck_id: int) -> Card:
        card = Card(question=question, answer=answer, difficulty=difficulty, deck_id=deck_id, next_study=datetime.now())

        created_card_id = self.repository.add(card)
        return self.repository.get_by_id(created_card_id)

    def update(self, card_id: int, question: str, answer: str) -> Card:
        existing_card = self.repository.get_by_id(card_id)

        existing_card.question = question
        existing_card.answer = answer

        updated_card_id = self.repository.update(existing_card)
        return self.repository.get_by_id(updated_card_id)

    def update_study(self, card_id: int, difficulty: int):
        existing_card = self.repository.get_by_id(card_id)

        interval, repetitions, easy_factor = get_ire(existing_card, difficulty)

        existing_card.next_study = datetime.now() + timedelta(days=interval)
        existing_card.previous_interval = interval
        existing_card.repetitions = repetitions
        existing_card.previous_easy_factor = easy_factor
        self.repository.update(existing_card)

    def delete(self, card_id: int) -> None:
        self.repository.delete(card_id)

    def get_all_by_deck_id(self, deck_id: int) -> list[Card]:
        return self.repository.get_all_by_deck_id(deck_id)

    def get_by_id(self, card_id: int) -> Card | None:
        return self.repository.get_by_id(card_id)

    def get_today(self, deck_id: int) -> list[Card]:
        end_of_day = datetime.now().replace(hour=23, minute=59, second=59)
        return filter(lambda card: card.next_study <= end_of_day, self.get_all_by_deck_id(deck_id))
