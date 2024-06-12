from models.db import Token
from repositories.base_repository import BaseRepository


class TokenRepository(BaseRepository):
    def add(self, token: Token) -> int:
        with self.session_maker.begin() as session:
            session.add(token)
            session.flush()

            return token.id

    def delete(self, token_id: int) -> None:
        with self.session_maker.begin() as session:
            to_delete = session.query(Token).where(
                Token.id == token_id
            ).first()

            if to_delete:
                session.delete(to_delete)

    def get_bv_id(self, token_id: int) -> Token | None:
        with self.session_maker.begin() as session:
            token = session.query(Token).where(
                Token.id == token_id
            ).first()

            return token

    def get_by_hash(self, token_hash: str) -> Token | None:
        with self.session_maker.begin() as session:
            token = session.query(Token).where(
                Token.hash == token_hash
            ).first()

            return token

    def get_all_by_user_id(self, user_id: int, limit: int = 1000, offset: int = 0) -> list[Token]:
        with self.session_maker.begin() as session:
            token_list = session.query(Token).where(
                Token.user_id == user_id
            ).limit(limit).offset(offset).all()

            return token_list
