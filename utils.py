import datetime
from typing import Dict

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from passlib.context import CryptContext

from settings import settings
from models.models import User_Pydantic, Users, UserIn_Pydantic, CreateUserModel
import jwt


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(userid: int):
    return UserIn_Pydantic.from_queryset_single(Users.get(userid=userid))


async def create_user(user: UserIn_Pydantic) -> User_Pydantic:
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)



async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await Users.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: UserIn_Pydantic = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def add_user_to_db(user: CreateUserModel):
    """добавление в БД нового пользователя"""
    user.hashed_password = get_password_hash(user.password)
    new_user = await create_user(user)
    return new_user


def generate_token(user: Users):
    paylod = {'id': str(user.id),
              'datetime': str(datetime.datetime.now())}
    return jwt.encode(paylod, settings.jwt_secret)

def decode_token(token: str) -> Dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=['HS256'])

async def get_admin_user(token: str = Depends(oauth2_scheme)) -> Users:
    """метод получает данные текущего авторизованного пользователя и проверяет что он админ"""
    try:
        user = await Users.get_user_by_token(token)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='не валидный токен'
        )
    if user.superuser:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='не достаточно прав')

