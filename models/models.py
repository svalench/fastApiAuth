from typing import Type, Optional

from pydantic import BaseModel
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel


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

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash"]


User_Pydantic: Type[PydanticModel] = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)