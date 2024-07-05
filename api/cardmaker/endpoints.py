from enum import Enum, auto

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from SQLModel import select, Session
import os

from . import models

app = APIRouter()
engine = create_engine(os.getenv(DATABASE_URL))


@router.get("users")
async def get_users():
    with Session(engine) as session:
        statement = select(models.User)
        json_data = jsonable_encoder(session.exec(statement))
        return JSONResponse(content=json_data)


@roter.get("card-types")
async def get_tags():
    with Session(engine) as session:
        statement = select(models.CardType)
        json_data = jsonable_encoder(session.exec(statement))
        return JSONResponse(content=json_data)


@roter.get("tags")
async def get_tags():
    with Session(engine) as session:
        statement = select(models.Tag)
        json_data = jsonable_encoder(session.exec(statement))
        return JSONResponse(content=json_data)


@router.get("cards")
async def get_cards(
    user: int = None,
    card_type: int = None,
    tags: list[int] = None,
):
    with Session(engine) as session:
        statement = select(models.Card)
        if user:
            statement = statement.where(models.Card.user_id == user)
        if card_type:
            statement = statement.where(models.Card.card_type_id == card_type)
        if tags:
            ...
        json_data = jsonable_encoder(session.exec(statement))
        return JSONResponse(content=json_data)
