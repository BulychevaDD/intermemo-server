from fastapi import FastAPI, Request, Response

from consts.token_consts import COOKIES_TOKEN_NAME
from services.token_service import TokenService
from services.user_service import UserService


class AuthMiddleware:
    app: FastAPI
    user_service: UserService
    token_service: TokenService

    def __init__(self, app: FastAPI):
        self.user_service = UserService()
        self.token_service = TokenService()

        self._enrich_with_auth_middleware(app)

    def _enrich_with_auth_middleware(self, app: FastAPI) -> None:
        @app.middleware("http")
        async def middleware(request: Request, call_next):
            token_hash = request.cookies.get(COOKIES_TOKEN_NAME)

            if not token_hash:
                return Response(status_code=401, content="Token not found")

            is_token_valid = self.token_service.check_token_hash_and_delete_if_expired(token_hash)
            if not is_token_valid:
                response = Response(status_code=401, content="Invalid token")
                response.delete_cookie(COOKIES_TOKEN_NAME)
                return response

            user_id = self.token_service.get_user_id_by_token_hash(token_hash)
            user = self.user_service.get_by_user_id(user_id)
            request.state.user = user

            return await call_next(request)
