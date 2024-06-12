from datetime import datetime, timedelta

from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from controllers.base_controller import BaseController
from models.db import Deck
from models.dto import CreateDeckDto, UpdateDeckDto


class DeckController(BaseController):
    @staticmethod
    def _convert_deck_to_dto(deck: Deck, statistics: object = None) -> object:
        return {
            'id': deck.id,
            'name': deck.name,
            'description': deck.description,
            'created_at': str(deck.created_at),
            'updated_at': str(deck.updated_at),
            'last_study': str(deck.last_study) if deck.last_study is not None else None,
            'statistics': statistics,
        }

    @staticmethod
    def _convert_decks_list_to_dto(decks_list: list[Deck]) -> object:
        return list(map(DeckController._convert_deck_to_dto, decks_list))

    def get_statistics(self, deck_id: int) -> object:
        deck_cards = self.card_service.get_all_by_deck_id(deck_id)

        cards_amount = len(deck_cards)
        cards_average_difficulty = sum(map(lambda card: card.difficulty, deck_cards)) / cards_amount if len(
            deck_cards) > 0 else 0
        cards_today = len(list(filter(lambda card: card.next_study.date() == datetime.today().date(), deck_cards)))

        tomorrow = (datetime.today() + timedelta(days=1)).date()
        cards_tomorrow = len(list(filter(lambda card: card.next_study.date() == tomorrow, deck_cards)))

        return {
            "cards_amount": cards_amount,
            "cards_average_difficulty": cards_average_difficulty,
            "cards_today": cards_today,
            "cards_tomorrow": cards_tomorrow,
        }

    def create(self, dto: CreateDeckDto, request: Request) -> JSONResponse | Response:
        if not BaseController.is_all_required_parameters_present(dto, 'name'):
            return Response(status_code=400, content="Missing required parameters")

        name, description = dto.name, dto.description
        user = BaseController.get_user_from_request(request)

        deck = self.deck_service.create(name=name, description=description, owner_id=user.id)

        return JSONResponse(DeckController._convert_deck_to_dto(deck), status_code=201)

    def update(self, deck_id: int, dto: UpdateDeckDto, request: Request) -> Response:
        if not BaseController.is_all_required_parameters_present(dto, 'name'):
            return Response(status_code=400, content="Missing required parameters")

        name, description = dto.name, dto.description
        user = BaseController.get_user_from_request(request)

        deck = self.deck_service.update(deck_id=deck_id, name=name, description=description)

        if deck is None or deck.owner_id != user.id:
            return Response(status_code=404, content="Not found")

        return JSONResponse(DeckController._convert_deck_to_dto(deck, self.get_statistics(deck_id)), status_code=200)

    def delete(self, deck_id: int, request: Request) -> Response:
        user = BaseController.get_user_from_request(request)

        deck = self.deck_service.get_by_id(deck_id)

        if deck is None or deck.owner_id != user.id:
            return Response(status_code=404, content="Not found")

        cards = self.card_service.get_all_by_deck_id(deck_id)
        for card in cards:
            self.card_service.delete(card.id)

        self.deck_service.delete(deck_id)
        return Response(status_code=204)

    def get_all(self, request: Request) -> JSONResponse:
        user = BaseController.get_user_from_request(request)
        decks = self.deck_service.get_all_by_owner(user.id)

        return JSONResponse(DeckController._convert_decks_list_to_dto(decks))

    def get_by_id(self, deck_id: int, request: Request) -> Response:
        user = BaseController.get_user_from_request(request)
        deck = self.deck_service.get_by_id(deck_id)

        if deck.owner_id != user.id:
            return Response(status_code=404, content="Not found")

        return JSONResponse(DeckController._convert_deck_to_dto(deck, self.get_statistics(deck_id)), status_code=200)
