from settings import Settings

settings = Settings()
TORTOISE_ORM = {
    "connections": {"default": settings.db_url},
    "apps": {
        "models": {
            "models": ["models.models",
                       "aerich.models"],
            "default_connection": "default",
        },
    },
}