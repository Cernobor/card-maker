from enum import Enum, auto

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os

from . import models

app = APIRouter()
engine = create_engine(os.getenv(DATABASE_URL))


@router.get("users")
async def get_users():
    users = select(models.User).all()
    json_data = jsonable_encoder(users)
    return JSONResponse(content=json_data)


@router.get("cards")
async def get_cards(
    user: int = None,
    type: int = None,
    tags: list[int] = None,
):
    cards = db.query(models.Card).filter()
