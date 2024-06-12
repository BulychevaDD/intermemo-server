from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request

from controllers.base_controller import BaseController
from models.db import Card
from models.dto import CreateCardDto, UpdateCardDto, StudyCardDto


class CardController(BaseController):
    @staticmethod
    def convert_card_to_dto(card: Card) -> object:
        return {
            "id": card.id,
            "question": card.question,
            "answer": card.answer,
            "deck_id": card.deck_id,
            "created_at": str(card.created_at),
            "updated_at": str(card.updated_at),
            "difficulty": card.difficulty,
            "next_study": str(card.next_study),
        }

    @staticmethod
    def convert_cards_list_to_dto(cards: list[Card]) -> object:
        return list(map(CardController.convert_card_to_dto, cards))

    def is_deck_owner_matches_current_user(self, deck_id: int, request: Request) -> bool:
        user = BaseController.get_user_from_request(request)
        deck = self.deck_service.get_by_id(deck_id)

        return user.id == deck.owner_id

    def create(self, deck_id: int, dto: CreateCardDto, request: Request) -> Response:
        if not BaseController.is_all_required_parameters_present(dto, 'question', 'answer', 'difficulty'):
            return Response(status_code=400, content="Missing required parameters")

        question, answer, difficulty = dto.question, dto.answer, dto.difficulty

        if not self.is_deck_owner_matches_current_user(deck_id, request):
            return Response(status_code=404, content="Not found")

        card = self.card_service.create(question, answer, difficulty, deck_id)
        return JSONResponse(self.convert_card_to_dto(card))

    def update(self, deck_id: int, card_id: int, dto: UpdateCardDto, request: Request) -> Response:
        if not BaseController.is_all_required_parameters_present(dto, 'question', 'answer'):
            return Response(status_code=400, content="Missing required parameters")

        question, answer = dto.question, dto.answer

        if not self.is_deck_owner_matches_current_user(deck_id, request):
            return Response(status_code=404, content="Not found")

        card = self.card_service.update(card_id, question, answer)
        if card is None:
            return Response(status_code=404, content="Not found")

        return JSONResponse(self.convert_card_to_dto(card))

    def delete(self, deck_id: int, card_id: int, request: Request) -> Response:
        if not self.is_deck_owner_matches_current_user(deck_id, request):
            return Response(status_code=404, content="Not found")

        card = self.card_service.get_by_id(card_id)

        if card is None:
            return Response(status_code=404, content="Not found")

        self.card_service.delete(card_id)
        return Response(status_code=204)

    def get_all_by_deck_id(self, deck_id: int, request: Request) -> Response:
        if not self.is_deck_owner_matches_current_user(deck_id, request):
            return Response(status_code=404, content="Not found")

        cards = self.card_service.get_all_by_deck_id(deck_id)

        return JSONResponse(CardController.convert_cards_list_to_dto(cards))

    def get_all_today(self, deck_id: int, request: Request) -> Response:
        if not self.is_deck_owner_matches_current_user(deck_id, request):
            return Response(status_code=404, content="Not found")

        cards = self.card_service.get_today(deck_id)

        return JSONResponse(CardController.convert_cards_list_to_dto(cards))

    def study_card(self, deck_id: int, card_id: int, dto: StudyCardDto, request: Request) -> Response:
        if not BaseController.is_all_required_parameters_present(dto, 'difficulty'):
            return Response(status_code=400, content="Missing required parameters")

        difficulty = dto.difficulty

        if not self.is_deck_owner_matches_current_user(deck_id, request):
            return Response(status_code=404, content="Not found")

        self.card_service.update_study(card_id, difficulty)
        self.deck_service.set_last_study(deck_id)

        return Response(status_code=200)
