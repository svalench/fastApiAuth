from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist

from models.models import Users, UserIn_Pydantic
from utils import get_current_active_user, get_password_hash, verify_password

router = APIRouter(
    prefix='',
    tags=["Authorization"],
)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await UserIn_Pydantic.from_queryset_single(Users.get(username=form_data.username))
    except DoesNotExist as e:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    ee = verify_password(form_data.password, user.hashed_password)
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: UserIn_Pydantic = Depends(get_current_active_user)):
    return current_user
