from fastapi import FastAPI
from fastapi.requests import Request
from controllers.user_controller import UserController
from models.dto import LoginUserDto, CreateUserDto


class UserRouter:
    controller: UserController

    def __init__(self, app: FastAPI) -> None:
        super().__init__()
        self.controller = UserController()
        self._init_routes(app)

    def _init_routes(self, app: FastAPI) -> None:
        @app.post('/users/login')
        def login(_: Request, dto: LoginUserDto):
            return self.controller.login(dto)

        @app.post('/users/register')
        def register(_: Request, dto: CreateUserDto):
            return self.controller.register(dto)

        @app.post('/users/logout')
        def logout(request: Request):
            return self.controller.logout(request)
