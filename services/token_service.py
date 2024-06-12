from datetime import datetime
from hashlib import sha256
from random import randint

from models.db import Token
from repositories.token_repository import TokenRepository


class TokenService:
    repository: TokenRepository

    def __init__(self) -> None:
        self.repository = TokenRepository()

    @staticmethod
    def _generate_token_hash():
        timestamp_now = datetime.now().timestamp()
        random_number = randint(1, 100000)
        return sha256(f"${str(random_number)}${str(timestamp_now)}".encode()).hexdigest()

    def create_for_user_id(self, user_id: int, expires: datetime) -> Token:
        token = Token(
            user_id=user_id,
            hash=TokenService._generate_token_hash(),
            expires=expires
        )

        created_user_id = self.repository.add(token)
        return self.repository.get_bv_id(created_user_id)

    def get_all_by_user_id(self, user_id: int) -> list[Token]:
        return self.repository.get_all_by_user_id(user_id)

    def delete(self, token: Token) -> None:
        self.repository.delete(token.id)

    def get_by_hash(self, token_hash: str) -> Token | None:
        return self.repository.get_by_hash(token_hash)

    def delete_all_expired(self, tokens: list[Token]) -> list[Token]:
        return list(map(self.delete_if_expired, tokens))

    def delete_if_expired(self, token: Token) -> Token | None:
        now = datetime.now()
        if token.expires < now:
            self.delete(token)
            return None

        return token

    def check_token_hash_and_delete_if_expired(self, token_hash: str) -> bool:
        token = self.get_by_hash(token_hash)

        if not token:
            return False

        checked_token = self.delete_if_expired(token)
        return checked_token is not None

    def get_user_id_by_token_hash(self, token_hash: str) -> int:
        token = self.get_by_hash(token_hash)

        return token.user_id
