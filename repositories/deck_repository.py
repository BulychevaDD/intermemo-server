from models.db import Deck
from repositories.base_repository import BaseRepository
from sqlalchemy import and_


class DeckRepository(BaseRepository):
    def add(self, deck: Deck) -> int:
        with self.session_maker.begin() as session:
            session.add(deck)
            session.flush()

            return deck.id

    def update(self, deck: Deck) -> int | None:
        with self.session_maker.begin() as session:
            deck_to_update = session.query(Deck).where(
                Deck.id == deck.id
            ).first()

            if deck_to_update:
                deck_to_update.name = deck.name
                deck_to_update.description = deck.description
                deck_to_update.last_study = deck.last_study

                return deck_to_update.id

    def delete(self, deck_id: int) -> None:
        with self.session_maker.begin() as session:
            to_delete = session.query(Deck).where(
                Deck.id == deck_id
            ).first()

            if to_delete:
                session.delete(to_delete)

    def get_by_name_and_owner(self, name: str, owner_id) -> Deck | None:
        with self.session_maker.begin() as session:
            deck = session.query(Deck).where(
                and_(Deck.name == name, Deck.owner_id == owner_id)
            ).first()

            return deck

    def get_by_id(self, deck_id: int) -> Deck | None:
        with self.session_maker.begin() as session:
            deck = session.query(Deck).where(
                Deck.id == deck_id
            ).first()

            return deck

    def get_all_by_owner(self, owner_id: int, limit: int = 1000, offset: int = 0) -> list[Deck]:
        with self.session_maker.begin() as session:
            decks = session.query(Deck).where(
                Deck.owner_id == owner_id
            ).order_by(Deck.created_at.desc()).limit(limit).offset(offset).all()

            return decks
