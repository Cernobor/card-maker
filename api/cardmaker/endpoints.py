"""
API endpoints.
"""

from datetime import datetime
from typing import Callable, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from sqlmodel import SQLModel

from . import models, statements
from .logger import Logger


router = APIRouter()
logger = Logger.get_instance()


class CreateTag(BaseModel):
    """
    Fields of tag of CreateCard model.
    """

    id:int
    name: str
    description: Optional[str]


class CreateCard(BaseModel):
    """
    Fields of request body of POST '/cardmaker/cards'.
    If no user ID provided, user is set to default user (Anonymous).
    """

    id: Optional[int]
    name: str
    fluff: Optional[str]
    effect: Optional[str]
    user_id: Optional[int]
    card_type_id: int
    in_set: bool
    set_name: Optional[str]
    tags: List[CreateTag | None]


async def save_or_raise_500(instance: SQLModel) -> SQLModel:
    """
    Save instance into database or raise HTTP exeption.

    Args:
        instance (SQLModel): instance of child class of SQLModel

    Returns:
        SQLModel: same child of SQLModel with updated parameters

    Raises:
        HTTP 500: when cannot save data into database
    """
    try:
        return await statements.save_into_db(instance)
    except IOError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=500, detail=f"An exception occurred: {e}"
        )


async def connect_tags_or_raise_500(tags, card_id):
    """
    Save new tags and connect existing tags or raise HTTP exeption.

    Args:
        tags (List[CreateTag]): list of tags to connect
        card_id (int): ID of card to connect

    Raises:
        HTTP 500: when cannot save data into database
    """
    try:
        await statements.connect_tags_with_card(tags, card_id)
    except IOError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=500, detail=f"An exception occurred: {e}"
        )


async def delete_or_raise_500(instance: SQLModel):
    """
    Delete instance in database or raise HTTP exeption.

    Args:
        instance (SQLModel): instance of child class of SQLModel

    Raises:
        HTTP 500: when cannot delete data in database
    """
    try:
        await statements.delete_id_db(instance)
    except IOError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=500, detail=f"An exception occurred: {e}"
        )


async def get_or_raise_404(get_function: Callable, *args) -> SQLModel:
    """
    Get instance from databse or raise HTTP exeption.

    Args:
        get_function (Callable): function for getting data
        args (): arguments for 'get_function'

    Returns:
        SQLModel: requested instance of child class of SQLModel

    Raises:
        HTTP 500: when cannot delete data in database
    """
    data = await get_function(*args)
    if not data:
        logger.warning("Resource not found.")
        raise HTTPException(status_code=404, detail="Resource not found.")
    return data


@router.get("/users")
async def get_users():
    """
    Get list of all users and their ids.

    Returns:
        json response with status code 200: list of all users

    Raises:
        HTTP 500: database error
    """
    json_data = jsonable_encoder(await get_or_raise_404(statements.get_users))
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
        await get_or_raise_404(statements.get_card_types)
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
    json_data = jsonable_encoder(await get_or_raise_404(statements.get_tags))
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
    cards = await statements.get_filtered_cards(
        user_id=user_id, card_type_id=card_type_id, tags=tags
    )
    if not cards:
        logger.warning("Invalid resource requested in GET '/cards'")
        raise HTTPException(
            status_code=404,
            detail="Resource does not exist!",
        )
    cards = [
        CreateCard(
            id=card.id,
            name=card.name,
            fluff=card.fluff,
            effect=card.effect,
            user_id=card.user_id,
            card_type_id=card.card_type_id,
            in_set=card.in_set,
            set_name=card.set_name,
            tags=await get_or_raise_404(statements.get_tags_of_card, card.id),
        )
        for card in cards
    ]
    json_data = jsonable_encoder(cards)
    logger.info("Cards requested, response successful.")
    return JSONResponse(content=json_data, status_code=200)


@router.get("/cards/{card_id}")
async def get_card(card_id: int):
    """
    Get card information by card ID.

    Args:
        card_id (int): card ID

    Returns:
        json response with status code 200: card information

    Raises:
        HTTP 500: database error
    """
    card = await get_or_raise_404(statements.get_card_by_id, card_id)
    return_data = CreateCard(
            id=card.id,
            name=card.name,
            fluff=card.fluff,
            effect=card.effect,
            user_id=card.user_id,
            card_type_id=card.card_type_id,
            in_set=card.in_set,
            set_name=card.set_name,
            tags=await get_or_raise_404(statements.get_tags_of_card, card.id))
    return JSONResponse(content=jsonable_encoder(return_data), status_code=200)


@router.post("/cards")
async def create_card(data: CreateCard):
    """
    Create new card and save it into database.

    Args:
        card_data (CreateCard):
                json request body,field are defined in CreateCard

    Returns:
        json response with status code 201:
                success message and ID of created card

    Raises:
        HTTP 500: database error
        HTTP 404: invalid user ID or card type ID
    """
    user = await get_or_raise_404(
        statements.get_user_by_id_or_default, data.user_id
    )
    await get_or_raise_404(statements.get_card_type_by_id, data.card_type_id)
    card = await save_or_raise_500(
        models.Card(
            name=data.name,
            fluff=data.fluff,
            effect=data.effect,
            user_id=user.id,
            card_type_id=data.card_type_id,
            in_set=data.in_set,
            set_name=data.set_name,
        )
    )
    data.tags.append(
        models.Tag(name=str(datetime.now().year), description=None)
    )
    await connect_tags_or_raise_500(data.tags, card.id)
    response = {"status": "successfully created", "card_id": card.id}
    logger.info(f"New card {card.name} created!")
    return JSONResponse(content=response, status_code=201)


@router.put("/cards/{card_id}")
async def update_card(card_id: int, data: CreateCard):
    """
    Update an existing card and save it into database.

    Args:
        card_data (Card): json request body, field are defined in models.Card

    Returns:
        json response with status code 204: success message

    Raises:
        HTTP 500: database error
        HTTP 404: invalid card ID
    """
    card = await get_or_raise_404(statements.get_card_by_id, card_id)
    card.name = data.name
    card.fluff = data.fluff
    card.effect = data.effect
    card.in_set = data.in_set
    card.set_name = data.set_name
    if data.tags:
        await connect_tags_or_raise_500(data.tags, card_id)
    await save_or_raise_500(card)
    logger.info(f"New card {card.name} updated!")
    response = {"status": "success", "card": card_id}
    return JSONResponse(content=response, status_code=200)


@router.delete("/cards/{card_id}")
async def delete_card(card_id: int):
    """
    Delete an existing card in the database.

    Args:
        card_data (Card): json request body, field are defined in models.Card

    Returns:
        json response with status code 204: success message

    Raises:
        HTTP 500: database error
        HTTP 404: invalid card ID
    """
    card = await get_or_raise_404(statements.get_card_by_id, card_id)
    await delete_or_raise_500(card)
    logger.info(f"New card {card.name} deleted!")
    response = {"status": "success", "card": card_id}
    return JSONResponse(content=response, status_code=200)


@router.post("/users")
async def create_user(username: str):
    """
    Create new user and save it into database.

    Args:
        username (str): name of new created user

    Returns:
        json response: success message and ID of created user

    Raises:
        HTTP 500: database error
        HTTP 404: invalid card ID
    """
    if await statements.get_user_by_name(username):
        raise HTTPException(
            status_code=403, detail=f"User with name {username} already exists!"
        )
    user = await save_or_raise_500(models.User(name=username))
    response = {"status": "success", "user_id": user.id}
    logger.info(f"New user {user.name} created!")
    return JSONResponse(content=response, status_code=200)
