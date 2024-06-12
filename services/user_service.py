from passlib.context import CryptContext

from exceptions.base_exceptions import EntityAlreadyExistsException
from models.db import User
from repositories.user_repository import UserRepository


class UserService:
    repository: UserRepository
    crypt_context: CryptContext

    def __init__(self) -> None:
        self.repository = UserRepository()

        self.crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def create(self, username: str, password: str) -> User:
        existing_user = self.repository.get_by_username(username)

        if existing_user:
            raise EntityAlreadyExistsException()

        user = User(
            username=username,
            password_hash=self.crypt_context.hash(password),
        )

        created_user_id = self.repository.add(user)
        return self.repository.get_bv_id(created_user_id)

    def get_by_username_and_password(self, username: str, password: str) -> User | None:
        user = self.repository.get_by_username(username)

        if not user:
            return None

        if self.crypt_context.verify(password, user.password_hash):
            return user

        return None

    def is_username_exists(self, username: str) -> bool:
        return self.repository.get_by_username(username) is not None

    def get_by_user_id(self, user_id: int) -> User | None:
        return self.repository.get_bv_id(user_id)
