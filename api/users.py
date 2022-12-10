from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

from models.models import Users, UserIn_Pydantic, User_Pydantic, CreateUserModel
from utils import get_current_active_user, get_password_hash, add_user_to_db

router = APIRouter(
    prefix='/users',
    tags=["Users API"],
)

class Status(BaseModel):
    message: str



@router.get("/users", response_model=List[User_Pydantic])
async def get_users(limit: int = 10, offset: int = 0):
    return await User_Pydantic.from_queryset(Users.all().limit(limit).offset(offset))


@router.post("/users", response_model=User_Pydantic)
async def create_user(user: CreateUserModel):
    user_obj = await add_user_to_db(user)
    return user_obj


@router.get(
    "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.put(
    "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserIn_Pydantic):
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.delete("/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")

