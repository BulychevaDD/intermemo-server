from dataclasses import dataclass


@dataclass
class CreateUserDto:
    username: str
    password: str


@dataclass
class LoginUserDto:
    username: str
    password: str


@dataclass
class CreateDeckDto:
    name: str
    description: str


@dataclass
class UpdateDeckDto:
    name: str
    description: str


@dataclass
class CreateCardDto:
    question: str
    answer: str
    difficulty: int


@dataclass
class UpdateCardDto:
    question: str
    answer: str


@dataclass
class StudyCardDto:
    difficulty: int
