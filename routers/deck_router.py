from fastapi import FastAPI
from fastapi.requests import Request

from controllers.card_controller import CardController
from controllers.deck_controller import DeckController
from models.dto import CreateDeckDto, UpdateDeckDto, CreateCardDto, UpdateCardDto, StudyCardDto


class DeckRouter:
    deck_controller: DeckController
    card_controller: CardController

    def __init__(self, app: FastAPI) -> None:
        super().__init__()

        self.deck_controller = DeckController()
        self.card_controller = CardController()

        self._init_routes(app)

    def _init_routes(self, app: FastAPI) -> None:
        @app.post('/decks')
        def create_deck(request: Request, dto: CreateDeckDto):
            return self.deck_controller.create(dto, request)

        @app.get('/decks')
        def get_decks(request: Request):
            return self.deck_controller.get_all(request)

        @app.get('/decks/{deck_id}')
        def get_deck(request: Request):
            return self.deck_controller.get_by_id(request.path_params.get('deck_id'), request)

        @app.put('/decks/{deck_id}')
        def update_deck(request: Request, dto: UpdateDeckDto):
            return self.deck_controller.update(request.path_params.get('deck_id'), dto, request)

        @app.delete('/decks/{deck_id}')
        def delete_deck(request: Request):
            return self.deck_controller.delete(request.path_params.get('deck_id'), request)

        @app.get('/decks/{deck_id}/cards')
        def get_deck_cards(request: Request):
            return self.card_controller.get_all_by_deck_id(request.path_params.get('deck_id'), request)

        @app.post('/decks/{deck_id}/cards')
        def create_card(request: Request, dto: CreateCardDto):
            return self.card_controller.create(request.path_params.get('deck_id'), dto, request)

        @app.post('/decks/{deck_id}/cards/{card_id}/study')
        def create_card(request: Request, dto: StudyCardDto):
            return self.card_controller.study_card(
                request.path_params.get('deck_id'), request.path_params.get('card_id'), dto, request
            )

        @app.put('/decks/{deck_id}/cards/{card_id}')
        def update_card(request: Request, dto: UpdateCardDto):
            return self.card_controller.update(
                request.path_params.get('deck_id'), request.path_params.get('card_id'), dto, request
            )

        @app.delete('/decks/{deck_id}/cards/{card_id}')
        def delete_card(request: Request):
            return self.card_controller.delete(
                request.path_params.get('deck_id'), request.path_params.get('card_id'), request
            )

        @app.get('/decks/{deck_id}/study')
        def get_deck_study(request: Request):
            return self.card_controller.get_all_today(request.path_params.get('deck_id'), request)
