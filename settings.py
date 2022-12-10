from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "UserAuth API"
    debug: bool = False
    description: str = ''
    jwt_secret: str = '345345ergfdt54egrbdfg@#@#$@fgdfg44'
    admins_email: List[str] = ['chitsalex@gmail.com']
    items_per_user: int = 50
    db_url: str = 'sqlite://db.sqlite3'

    class Config:
        env_file = "app/.env"

settings = Settings()
