"""
Some usefull functions for API endpoints
"""

from typing import Callable

from fastapi import HTTPException
from sqlmodel import SQLModel

from . import models
from .logger import Logger
from .database import CardMakerDatabase


logger = Logger.get_instance()
database = CardMakerDatabase()


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
        return await database.save_into_db(instance)
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
        await database.connect_tags_with_card(tags, card_id)
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
        await database.delete_id_db(instance)
    except IOError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=500, detail=f"An exception occurred: {e}"
        )


async def get_or_raise_404(
    get_function: Callable, instance, *args, **kwargs
) -> SQLModel:
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
    logger.debug(args)
    data = await get_function(instance, *args, **kwargs)
    if not data:
        logger.warning("Resource not found.")
        raise HTTPException(status_code=404, detail="Resource not found.")
    return data
