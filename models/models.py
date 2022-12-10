from typing import Type, Optional, Self

import jwt
from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel

from settings import settings


class CreateUserModel(BaseModel):
    username: str
    password: str
    repeat_password: str
    hashed_password: Optional[str]


class Users(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=50, null=True)
    second_name = fields.CharField(max_length=50, null=True)
    family_name = fields.CharField(max_length=50, null=True)
    superuser = fields.BooleanField(default=False)
    disabled = fields.BooleanField(default=False)
    category = fields.CharField(max_length=30, default="misc")
    hashed_password = fields.CharField(max_length=1028, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def full_name(self) -> str:
        """
        Returns the best name
        """
        if self.name or self.family_name:
            return f"{self.name or ''} {self.family_name or ''}".strip()
        return self.username

    @classmethod
    async def get_user_by_token(cls, token: str):
        return await cls.get(id=jwt.decode(token, settings.jwt_secret, algorithms=['HS256']).get('id'))


    async def check_self(self, user_id, user) -> Self:
        if self.superuser:
            return True
        if user_id == self.id and (not user or not user.superuser):
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Отказано в доступе')

    class Meta:
        ordering = ['-id']

    class PydanticMeta:
        computed = ["full_name"]


User_Pydantic: Type[PydanticModel] = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True, optional=['username'])
UserFront_Pydantic = pydantic_model_creator(Users, name="UserFront", exclude=['hashed_password', 'superuser'])