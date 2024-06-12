from models.db import Card
from repositories.base_repository import BaseRepository


class CardRepository(BaseRepository):
    def add(self, card) -> int:
        with self.session_maker.begin() as session:
            session.add(card)
            session.flush()

            return card.id

    def update(self, card: Card) -> int | None:
        with self.session_maker.begin() as session:
            card_to_update = session.query(Card).where(
                Card.id == card.id
            ).first()

            if card_to_update:
                card_to_update.question = card.question
                card_to_update.answer = card.answer
                card_to_update.next_study = card.next_study
                card_to_update.repetitions = card.repetitions
                card_to_update.previous_interval = card.previous_interval
                card_to_update.previous_easy_factor = card.previous_easy_factor

                return card_to_update.id

    def delete(self, card_id: int) -> None:
        with self.session_maker.begin() as session:
            card_to_delete = session.query(Card).where(
                Card.id == card_id
            ).first()

            if card_to_delete:
                session.delete(card_to_delete)

    def get_by_id(self, card_id) -> Card | None:
        with self.session_maker.begin() as session:
            card = session.query(Card).where(
                Card.id == card_id
            ).first()

            return card

    def get_all_by_deck_id(self, deck_id: int, limit: int = 1000, offset: int = 0) -> list[Card]:
        with self.session_maker.begin() as session:
            cards = session.query(Card).where(
                Card.deck_id == deck_id
            ).order_by(Card.created_at.desc()).limit(limit).offset(offset).all()

            return cards
