from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from models.db import Base
from utils.environment import get_environment_variable


class BaseRepository:
    engine: Engine
    session_maker: sessionmaker[Session]

    def __init__(self) -> None:
        connection_string = get_environment_variable('DB_CONNECTION_STRING')

        self.engine = create_engine(connection_string)
        self.session_maker = sessionmaker(bind=self.engine, expire_on_commit=False)

    def create_database(self) -> None:
        Base.metadata.create_all(self.engine)
