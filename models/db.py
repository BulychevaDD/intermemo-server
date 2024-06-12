from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Token(Base):
    __tablename__ = 'tokens'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'))
    hash = Column('hash', String(256), unique=True)
    expires = Column('expires', DateTime())


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    username = Column('username', String(32), unique=True)
    password_hash = Column('password', String(256))


class Deck(Base):
    __tablename__ = 'decks'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    owner_id = Column('owner_id', Integer(), ForeignKey('users.id'))
    name = Column('name', String(32), nullable=False)
    description = Column('description', String(256))
    created_at = Column('created_at', DateTime(), default=current_timestamp())
    updated_at = Column('updated_at', DateTime(), default=current_timestamp(), onupdate=current_timestamp())
    last_study = Column('last_study', DateTime())


class Card(Base):
    __tablename__ = 'cards'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    question = Column('question', String(256), nullable=False)
    answer = Column('answer', String(256), nullable=False)
    created_at = Column('created_at', DateTime(), default=current_timestamp())
    updated_at = Column('updated_at', DateTime(), default=current_timestamp(), onupdate=current_timestamp())
    deck_id = Column('deck_id', Integer(), ForeignKey('decks.id'))
    next_study = Column('next_study', DateTime())
    difficulty = Column('difficulty', Integer())
    repetitions = Column('repetitions', Integer(), default=0)
    previous_easy_factor = Column('previous_easy_factor', Float(), default=2.5)
    previous_interval = Column('previous_interval', Integer(), default=0)
