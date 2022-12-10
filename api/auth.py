from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist

from models.models import Users, UserIn_Pydantic, UserFront_Pydantic
from utils import get_current_active_user, get_password_hash, verify_password, generate_token

router = APIRouter(
    prefix='',
    tags=["Authorization"],
)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """aвторизауия пользователя по Auth2"""
    try:
        user = await Users.get(username=form_data.username)
    except DoesNotExist as e:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"access_token": generate_token(user), "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: Users = Depends(get_current_active_user)):
    return UserFront_Pydantic.from_orm(current_user)
