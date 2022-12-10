from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from api import auth, users
from models.models import User_Pydantic, UserIn_Pydantic, Users
from settings import settings
from utils import get_user


app = FastAPI(
    debug=settings.debug,
    title=settings.app_name,
    description=settings.description
)
app.include_router(auth.router)
app.include_router(users.router)

@app.get('/')
async def aaa():
    return {**settings.dict()}

register_tortoise(
    app,
    db_url=settings.db_url,
    modules={"models": ["models.models", "aerich.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)