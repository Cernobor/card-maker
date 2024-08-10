"""
API endpoints.
"""

from datetime import datetime, timedelta
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPBasicCredentials

from . import models, security, utils
from .database import CardMakerDatabase
from .logger import Logger

router = APIRouter()
logger = Logger.get_instance()
database = CardMakerDatabase()


@router.get("/users")
async def get_users():
    """
    Get list of all users and their ids.

    Returns:
        json response with status code 200: list of all users

    Raises:
        HTTP 500: database error
    """
    json_data = jsonable_encoder(
        await utils.get_or_raise_404(CardMakerDatabase.get_users, database)
    )
    logger.info("Users requested, response successful.")
    return JSONResponse(content=json_data, status_code=200)


@router.get("/card-types")
async def get_card_types():
    """
    Get list of all card types and their ids.

    Returns:
        json response with status code 200: list of all card types

    Raises:
        HTTP 500: database error
    """
    json_data = jsonable_encoder(
        await utils.get_or_raise_404(CardMakerDatabase.get_card_types, database)
    )
    logger.info("Card types requested, response successful.")
    return JSONResponse(content=json_data, status_code=200)


@router.get("/tags")
async def get_tags():
    """
    Get list of all tags and their ids.

    Returns:
        json response with status code 200: list of all tags

    Raises:
        HTTP 500: database error
    """
    json_data = jsonable_encoder(
        await utils.get_or_raise_404(CardMakerDatabase.get_tags, database)
    )
    logger.info("Tags requested, response successful.")
    return JSONResponse(content=json_data, status_code=200)


@router.get("/cards")
async def get_cards(
    user_id: int | None = None,
    card_type_id: int | None = None,
    tags: str | None = None,
):
    """
    Get list of cards filtered by query parameters.

    Args:
        user_id (int|None, default: None): user ID (model User)
        card_type_id (int|None, default: None): card type ID (model CardType)
        tags (str|None, default: None): tag names splitted by ','

    Returns:
        json response with status code 200: filtered list of cards

    Raises:
        HTTP 500: database error
    """
    cards = await database.get_filtered_cards(
        user_id=user_id, card_type_id=card_type_id, tags=tags
    )
    if not cards:
        logger.warning("Invalid resource requested in GET '/cards'")
    cards_new = []
    for card in cards:
        tags = [
            models.TagBase.model_validate(tag)
            for tag in await utils.get_or_raise_404(
                CardMakerDatabase.get_tags_of_card, database, card.id
            )
        ]
        cards_new.append(
            models.CardGet.model_validate(
                card.model_dump(), update={"tags": tags}
            )
        )
    logger.info("Cards requested, response successful.")
    return JSONResponse(content=jsonable_encoder(cards_new), status_code=200)


@router.get("/cards/{card_id}")
async def get_card_by_id(card_id: int):
    """
    Get card information by card ID.

    Args:
        card_id (int): card ID

    Returns:
        json response with status code 200: card information

    Raises:
        HTTP 500: database error
    """
    card = await utils.get_or_raise_404(
        CardMakerDatabase.get_card_by_id, database, card_id
    )
    card = models.CardGet.model_validate(
        card.model_dump(),
        update={
            "tags": [
                models.TagBase.model_validate(tag)
                for tag in await utils.get_or_raise_404(
                    CardMakerDatabase.get_tags_of_card, database, card.id
                )
            ]
        },
    )
    return JSONResponse(content=jsonable_encoder(card), status_code=200)


@router.post("/cards", dependencies=[Depends(security.JWTBearer())])
async def create_card(data: models.CardCreate):
    """
    Create new card and save it into database.

    Args:
        data (models.CardCreate):
                json request body, fields are defined in models.CardCreate

    Returns:
        json response with status code 201:
                success message and ID of created card

    Raises:
        HTTP 500: database error
        HTTP 404: invalid user ID or card type ID
    """
    user = await utils.get_or_raise_404(
        CardMakerDatabase.get_user_by_id_or_default, database, data.user_id
    )
    data.user_id = user.id
    await utils.get_or_raise_404(
        CardMakerDatabase.get_card_type_by_id, database, data.card_type_id
    )
    card = await utils.save_or_raise_500(models.Card.model_validate(data))
    data.tags.append(
        models.Tag(name=str(datetime.now().year), description="year")
    )
    await utils.connect_tags_or_raise_500(data.tags, card.id)
    logger.info(f"New card {card.name} created!")
    return JSONResponse(
        content={"status": "successfully created", "card_id": card.id},
        status_code=201,
    )


@router.put("/cards/{card_id}", dependencies=[Depends(security.JWTBearer())])
async def update_card(card_id: int, data: models.CardUpdate):
    """
    Update an existing card and save it into database.

    Args:
        data (models.CardCreate):
                json request body, field are defined in models.CardCreate

    Returns:
        response with status code 204

    Raises:
        HTTP 500: database error
        HTTP 404: invalid card ID
    """
    card = await utils.get_or_raise_404(
        CardMakerDatabase.get_card_by_id, database, card_id
    )
    if data.tags:
        await utils.connect_tags_or_raise_500(data.tags, card_id)
    await utils.save_or_raise_500(card.sqlmodel_update(data.model_dump()))
    logger.info(f"New card {card.name} updated!")
    return Response(status_code=204)


@router.delete("/cards/{card_id}", dependencies=[Depends(security.JWTBearer())])
async def delete_card(card_id: int):
    """
    Delete an existing card in the database.

    Args:
        card_id (int): id of card to delete

    Returns:
        response with status code 204

    Raises:
        HTTP 500: database error
        HTTP 404: invalid card ID
    """
    card = await utils.get_or_raise_404(
        CardMakerDatabase.get_card_by_id, database, card_id
    )
    await utils.delete_or_raise_500(card)
    logger.info(f"New card {card.name} deleted!")
    return Response(status_code=204)


@router.post("/users")
async def create_user(data: models.UserCreate):
    """
    Create new user and save it into database.

    Args:
        data (models.UserCreate):
                json request body, field are defined in models.UserCreate

    Returns:
        json response with status code 201:
                success message and ID of created user

    Raises:
        HTTP 500: database error
        HTTP 401" wron API key
        HTTP 403: existing username
    """
    if not security.verify_api_key(data.api_key):
        raise HTTPException(status_code=401, detail="Wrong API key!")
    if await database.get_user_by_name(data.username):
        raise HTTPException(
            status_code=403,
            detail=f"User with name {data.username} already exists!",
        )
    logger.info(data)
    hashed_password, salt = security.hash_password(data.password)
    user = await utils.save_or_raise_500(
        models.User.model_validate(
            data,
            update={
                "hashed_password": hashed_password,
                "salt": salt,
            },
        )
    )
    response = {"status": "success", "user_id": user.id}
    logger.info(f"New user {user.username} created!")
    return JSONResponse(content=response, status_code=201)


@router.post("/users/me")
async def get_access_token(
    credentials: Annotated[HTTPBasicCredentials, Depends(security.http_basic)]
):
    """
    Generate JWT token for current user.

    Args:
        credentials (HTTPBasicCredentials): username and password

    Returns:
        json response with status code 200:
                token with token type 'bearer'

    Raises:
        HTTP 401: wrong credentials
    """
    user = await security.authenticate(
        credentials.username, credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Wrong username or password!",
            headers={"WWW-Authenticate": "Basic"},
        )
    response = jsonable_encoder(
        models.Token(
            access_token=security.create_access_token(
                user, datetime.now() + timedelta(days=15)
            ),
            token_type="bearer",
            user_id=user.id,
        )
    )
    return JSONResponse(status_code=200, content=response)
