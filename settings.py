from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "UserAuth API"
    debug: bool = False
    description: str = ''
    admins_email: List[str] = ['chitsalex@gmail.com']
    items_per_user: int = 50
    db_url: str = 'sqlite:///base.db'
