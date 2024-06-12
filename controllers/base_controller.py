from dataclasses import dataclass, asdict

from fastapi.requests import Request

from models.db import User
from services.card_service import CardService
from services.deck_service import DeckService
from services.token_service import TokenService
from services.user_service import UserService


class BaseController:
    token_service: TokenService
    user_service: UserService
    deck_service: DeckService
    card_service: CardService

    def __init__(self):
        self.token_service = TokenService()
        self.user_service = UserService()
        self.deck_service = DeckService()
        self.card_service = CardService()

    @staticmethod
    def is_all_required_parameters_present(parameters: dataclass, *required_keys: str) -> bool:
        for required_key in required_keys:
            if required_key not in asdict(parameters).keys() or getattr(parameters, required_key) is None:
                return False

        return True

    @staticmethod
    def get_user_from_request(request: Request) -> User:
        return request.state.user
