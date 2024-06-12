from models.db import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def add(self, user: User) -> int:
        with self.session_maker.begin() as session:
            session.add(user)
            session.flush()

            return user.id

    def get_bv_id(self, user_id: int) -> User | None:
        with self.session_maker.begin() as session:
            user = session.query(User).where(
                User.id == user_id
            ).first()

            return user

    def get_by_username(self, username: str) -> User | None:
        with self.session_maker.begin() as session:
            user = session.query(User).where(
                User.username == username
            ).first()

            return user
