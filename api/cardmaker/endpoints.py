import logging
import os
from datetime import datetime
from enum import Enum, auto
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, create_engine, select

from . import models
from .logger import setup_logger


class CreateCard(BaseModel):
    name: str
    fluff: Optional[str]
    effect: Optional[str]
    user_id: Optional[int]
    card_type_id: int
    tags: list["str"]


router = APIRouter()
engine = create_engine("mysql+mysqlconnector://root:root@db:3306/Cardmaker")
logger = setup_logger("my_logger", "app.log")


@router.get("/users")
async def get_users():
    try:
        with Session(engine) as session:
            statement = select(models.User)
            result = session.execute(statement)
            json_data = jsonable_encoder(result.scalars().all())
            logger.info(f"Users requested, response successful.")
            return JSONResponse(content=json_data, status_code=200)
    except Exception as e:
        logger.error(f"Database error: {e} in '/users'")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@router.get("/card-types")
async def get_card_types():
    try:
        with Session(engine) as session:
            statement = select(models.CardType)
            result = session.execute(statement)
            json_data = jsonable_encoder(result.scalars().all())
            logger.info(f"Card types requested, response successful.")
            return JSONResponse(content=json_data)
    except Exception as e:
        logger.error(f"Database error: {e} in '/card-types'")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/tags")
async def get_tags():
    try:
        with Session(engine) as session:
            statement = select(models.Tag)
            result = session.execute(statement)
            json_data = jsonable_encoder(result.scalars().all())
            logger.info(f"Tags requested, response successful.")
            return JSONResponse(content=json_data, status_code=200)
    except Exception as e:
        logger.error(f"Database error: {e} in '/tags'")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/cards")
async def get_cards(
    user: int = None,
    card_type: int = None,
    tags: str = None,
):
    try:
        with Session(engine) as session:
            statement = select(models.Card)
            if user:
                statement = statement.where(models.Card.user_id == user)
            if card_type:
                statement = statement.where(models.Card.card_type_id == card_type)
            if tags:
                ...
            result = session.execute(statement)
            json_data = jsonable_encoder(result.scalars().all())
            logger.info(f"Cards requested, response successful.")
            return JSONResponse(content=json_data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/create/card")
async def create_card(card_data: CreateCard):
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
                raise HTTPException(status_code=404, detail=f"User with id {card_data.user_id} does not exist!")
            
            statement = select(models.CardType).where(
                models.CardType.id == card_data.card_type_id
            )
            card_type = session.exec(statement).first()
            if not card_type:
                logger.warning(f"Invalid card type id {card_data.card_type_id}.")
                raise HTTPException(status_code=404, detail=f"Card type with id {card_data.card_type_id} does not exist!")
            
            card = models.Card(
                name=card_data.name,
                fluff=card_data.fluff,
                effect=card_data.effect,
                user_id=card_data.user_id,
                card_type_id=card_data.card_type_id,
            )
            try:
                session.add(card)
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Database error: {e}")
                raise HTTPException(status_code=500, detail=f"An exception occurred: {e}")
            session.refresh(card)

            card_data.tags.append(str(datetime.now().year))
            for tag in card_data.tags:
                statement = select(models.Tag).where(models.Tag.name == tag)
                tag_instance = session.exec(statement).first()
                if not tag_instance:
                    try:
                        new_tag = models.Tag(name=tag, visible=False)
                        session.add(new_tag)
                        session.commit()
                        session.refresh(new_tag)
                        tag_instance = new_tag
                    except Exception as e:
                        logger.error(f"Database error: {e}")
                        session.rollback()
                        raise HTTPException(status_code=500, detail=f"An exception occurred: {e}")
                
                logger.info(f"tag: {tag_instance}")
                card_tag_relationship = models.CardTagRelationship(card_id=card.id, tag_id=tag_instance.id)
                session.add(card_tag_relationship)

            session.commit()

            response = {
                "status": "success",
                "card_id": card.id
            }
            logger.info(f"New card {card.name} created!")
            return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.error(f"Database error: {e} in '/create/card'")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/create/user")
async def create_user(username: str):
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
            response = {
                "status": "success",
                "card_id": user.id
            }
            logger.info(f"New user {user.name} created!")
            return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.error(f"Database error: {e} in '/create/user'")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
