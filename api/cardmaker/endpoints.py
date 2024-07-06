"""
API endpoints.
"""

import logging
import os
from datetime import datetime
from enum import Enum, auto
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, create_engine, select

from . import models
from .logger import setup_logger


class CreateTag(BaseModel):
    name: str
    visible: bool = False


class CreateCard(BaseModel):
    """
    Fields of request body of POST '/cardmaker/cards'.
    If no user ID provided, user is set to default user (Anonymous).
    """

    name: str
    fluff: Optional[str]
    effect: Optional[str]
    user_id: Optional[int]
    card_type_id: int
    tags: List[CreateTag|None]


router = APIRouter()
engine = create_engine(os.getenv("DATABASE_URL"))
logger = setup_logger("my_logger", "app.log")


@router.get("/users")
async def get_users():
    """
    Get list of all users and their ids.

    Returns:
        json response with status code 200: list of all users

    Raises:
        HTTP 500: database error
    """
    try:
        with Session(engine) as session:
            statement = select(models.User)
            result = session.execute(statement)
            json_data = jsonable_encoder(result.scalars().all())
            logger.info(f"Users requested, response successful.")
            return JSONResponse(content=json_data, status_code=200)
    except Exception as e:
        logger.error(f"Database error: {e} in GET '/users'")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.get("/card-types")
async def get_card_types():
    """
    Get list of all card types and their ids.

    Returns:
        json response with status code 200: list of all card types

    Raises:
        HTTP 500: database error
    """
    try:
        with Session(engine) as session:
            statement = select(models.CardType)
            result = session.execute(statement)
            json_data = jsonable_encoder(result.scalars().all())
            logger.info(f"Card types requested, response successful.")
            return JSONResponse(content=json_data)
    except Exception as e:
        logger.error(f"Database error: {e} in GET '/card-types'")
        raise HTTPException(status_code=500, detail=f"Database error: {e})")


@router.get("/tags")
async def get_tags():
    """
    Get list of all tags and their ids.

    Returns:
        json response with status code 200: list of all tags

    Raises:
        HTTP 500: database error
    """
    try:
        with Session(engine) as session:
            statement = select(models.Tag)
            result = session.execute(statement)
            json_data = jsonable_encoder(result.scalars().all())
            logger.info(f"Tags requested, response successful.")
            return JSONResponse(content=json_data, status_code=200)
    except Exception as e:
        logger.error(f"Database error: {e} in GET '/tags'")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.get("/cards")
async def get_cards(
    user: int|None = None,
    card_type: int|None = None,
    tags: str|None = None,
):
    """
    Get list of cards filtered by query parameters.

    Args:
        user (int|None, default: None): user ID (model User)
        card_type (int|None, default: None): card type ID (model CardType)
        tags (str|None, default: None): tag names splitted by ','

    Returns:
        json response with status code 200: filtered list of cards

    Raises:
        HTTP 500: database error
    """
    try:
        with Session(engine) as session:
            statement = select(models.Card)
            if user:
                statement = statement.where(models.Card.user_id == user)
            if card_type:
                statement = statement.where(models.Card.card_type_id == card_type)
            if tags:
                for tag in tags.split(","):
                    statement = statement.where(models.Tag.name == tag)
            result = session.execute(statement).scalars().all()
            if not result:
                logger.warning("Invalid value of one or more query params in GET '/cards'")
                raise HTTPException(
                    status_code=404,
                    detail="Resource does not exist!",
                )
            json_data = jsonable_encoder(result)
            logger.info(f"Cards requested, response successful.")
            return JSONResponse(content=json_data, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.post("/cards")
async def create_card(card_data: CreateCard):
    """
    Create new card and save it into database.

    Args:
        card_data (CreateCard): json request body, field are defined in CreateCard

    Returns:
        json response with status code 201: success message and ID of created card

    Raises:
        HTTP 500: database error
        HTTP 404: invalid user ID or card type ID
    """
    try:
        with Session(engine) as session:
            statement = (
                select(models.User).where(models.User.id == card_data.user_id)
                if card_data.user_id
                else select(models.User).where(models.User.name == "Anonymous")
            )
            user = session.exec(statement).first()
            if not user:
                logger.warning(f"Invalid user id {card_data.user_id}.")
                raise HTTPException(
                    status_code=404,
                    detail=f"User with id {card_data.user_id} does not exist!",
                )

            statement = select(models.CardType).where(
                models.CardType.id == card_data.card_type_id
            )
            card_type = session.exec(statement).first()
            if not card_type:
                logger.warning(f"Invalid card type id {card_data.card_type_id}.")
                raise HTTPException(
                    status_code=404,
                    detail=f"Card type with id {card_data.card_type_id} does not exist!",
                )

            card = models.Card(
                name=card_data.name,
                fluff=card_data.fluff,
                effect=card_data.effect,
                user_id=user.id,
                card_type_id=card_type.id,
            )
            try:
                session.add(card)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
                raise HTTPException(
                    status_code=500, detail=f"An exception occurred: {e}"
                )
            session.refresh(card)

            card_data.tags.append(models.Tag(
                name = str(datetime.now().year),
                visible = False
            ))
            for tag in card_data.tags:
                statement = select(models.Tag).where(models.Tag.name == tag.name)
                tag_instance = session.exec(statement).first()
                if not tag_instance:
                    try:
                        new_tag = models.Tag(name=tag.name, visible=tag.visible)
                        session.add(new_tag)
                        session.commit()
                        session.refresh(new_tag)
                        tag_instance = new_tag
                    except Exception as e:
                        logger.error(f"Database error: {e}")
                        session.rollback()
                        raise HTTPException(
                            status_code=500, detail=f"An exception occurred: {e}"
                        )

                card_tag_relationship = models.CardTagRelationship(
                    card_id=card.id, tag_id=tag_instance.id
                )
                session.add(card_tag_relationship)

            session.commit()

            response = {"status": "successfully created", "card_id": card.id}
            logger.info(f"New card {card.name} created!")
            return JSONResponse(content=response, status_code=201)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Database error: {e} in POST '/cards'")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.put("/cards/{card_id}")
def update_card(card_id: int, data: models.Card):
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
    try:
        with Session(engine) as session:
            statement = select(models.Card).where(models.Card.id == card_id)
            result = session.exec(statement).first()
            if not result:
                logger.warning(f"Invalid resource requested: card {card_id}.")
                raise HTTPException(
                    status_code=404,
                    detail=f"Invalid resource requested: card {card_id}."
                )
            result.name = data.name
            result.fluff = data.fluff
            result.effect = data.effect
            try:
                session.add(result)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
                raise HTTPException(
                    status_code=500, detail=f"An exception occurred: {e}"
                )

            response = {"status": "successfully updated"}
            logger.info(f"New card {result.name} updated!")
            return JSONResponse(content=response, status_code=204)

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Database error: {e} in PUT '/cards'")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.delete("/cards/{card_id}")
def delete_card(card_id: int):
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
    try:
        with Session(engine) as session:
            statement = select(models.Card).where(models.Card.id == card_id)
            result = session.exec(statement).first()
            if not result:
                logger.warning(f"Invalid resource requested: card {card_id}.")
                raise HTTPException(
                    status_code=404,
                    detail=f"Invalid resource requested: card {card_id}."
                )
            try:
                session.delete(result)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
                raise HTTPException(
                    status_code=500, detail=f"An exception occurred: {e}"
                )
            response = {"status": "successfully deleted"}
            logger.info(f"New card {result.name} deleted!")
            return JSONResponse(content=response, status_code=204)

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Database error: {e} in DELETE '/cards'")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


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
    """
    try:
        with Session(engine) as session:
            statement = select(models.User).where(models.User.name == username)
            users = session.exec(statement)
            if users.first():
                return HTTPException(f"User with username {username} already exists!")
            user = models.User(name=username)
            try:
                session.add(user)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
                return HTTPException(f"An exeption occured: {e}")
            session.refresh(user)
            response = {"status": "success", "card_id": user.id}
            logger.info(f"New user {user.name} created!")
            return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.error(f"Database error: {e} in POST '/users'")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
