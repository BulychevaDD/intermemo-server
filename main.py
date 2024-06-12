from fastapi import FastAPI
from middlewares.auth_middleware import AuthMiddleware
from routers.deck_router import DeckRouter
from routers.user_router import UserRouter

app = FastAPI(root_path='/api')

public_api = FastAPI()
private_api = FastAPI()

DeckRouter(private_api)
AuthMiddleware(private_api)

UserRouter(public_api)

app.mount('/public', public_api)
app.mount('/private', private_api)
