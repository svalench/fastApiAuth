from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from api import auth, users
from settings import settings


app = FastAPI(
    debug=settings.debug,
    title=settings.app_name,
    description=settings.description
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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