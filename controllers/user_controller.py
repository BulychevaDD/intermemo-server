from datetime import datetime

from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from consts.token_consts import COOKIES_TOKEN_NAME
from controllers.base_controller import BaseController
from exceptions.base_exceptions import EntityAlreadyExistsException
from models.db import User
from models.dto import CreateUserDto, LoginUserDto


class UserController(BaseController):
    session_ttl = 3600 * 24 * 30

    @staticmethod
    def _convert_user_to_dto(user: User) -> object:
        return {
            'username': user.username,
        }

    def _enrich_response_with_auth_cookie(self, response: Response, user: User) -> Response:
        new_token_expires = datetime.fromtimestamp(datetime.now().timestamp() + self.session_ttl)
        new_token = self.token_service.create_for_user_id(user.id, new_token_expires)

        response.set_cookie(COOKIES_TOKEN_NAME, new_token.hash, self.session_ttl)

        return response

    def register(self, dto: CreateUserDto) -> Response:
        if not BaseController.is_all_required_parameters_present(dto, 'username', 'password'):
            return Response(status_code=400, content="Missing username or password")

        username, password = dto.username, dto.password

        try:
            user = self.user_service.create(username, password)
        except EntityAlreadyExistsException:
            return Response(status_code=409, content="Username already exists")

        response = JSONResponse(UserController._convert_user_to_dto(user))

        return self._enrich_response_with_auth_cookie(response, user)

    def login(self, dto: LoginUserDto) -> Response:
        if not BaseController.is_all_required_parameters_present(dto, 'username', 'password'):
            return Response(status_code=400, content="Missing username or password")

        username, password = dto.username, dto.password

        existing_user = self.user_service.get_by_username_and_password(username, password)

        if not existing_user:
            return Response(status_code=400, content="Invalid username or password")

        existing_user_tokens = self.token_service.get_all_by_user_id(existing_user.id)
        self.token_service.delete_all_expired(existing_user_tokens)

        return self._enrich_response_with_auth_cookie(Response(), existing_user)

    def logout(self, request: Request) -> Response:
        token_hash = request.cookies.get(COOKIES_TOKEN_NAME)

        token = self.token_service.get_by_hash(token_hash)

        if token:
            self.token_service.delete(token)

        return Response()
