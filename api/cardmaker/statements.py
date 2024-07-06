"""
Functions for executing SQL statements.
"""

import logging
import os
from typing import List

from sqlmodel import Session, SQLModel, create_engine, select

from . import models

engine = create_engine(os.getenv("DATABASE_URL"))
logger = logging.getLogger()


async def get_users() -> List[models.User | None]:
    """
    Get all users from database.

    Returns:
        List[models.User|None]: list of all users in db
    """
    with Session(engine) as session:
        statement = select(models.User)
        return session.execute(statement).scalars().all()


async def get_card_types() -> List[models.CardType | None]:
    """
    Get all card types from database.

    Returns:
        List[models.CardType|None]: list of all card types in db
    """
    with Session(engine) as session:
        statement = select(models.CardType)
        return session.execute(statement).scalars().all()


async def get_tags() -> List[models.Tag | None]:
    """
    Get all tags from database.

    Returns:
        List[models.Tag|None]: list of all tags in db
    """
    with Session(engine) as session:
        statement = select(models.Tag)
        return session.execute(statement).scalars().all()


async def get_filtered_cards(
    user_id: int | None = None,
    card_type_id: int | None = None,
    tags: str | None = None,
) -> List[models.Card | None]:
    """
    Get cards filtered by user, card type and tags.

    Args:
        user_id (int|None, default: None): ID of user
                        (author of card, which should be returned)
        card_type_id (int|None, default: None): ID of user
                        (type of card, which should be returned)
        tags: (str|None, default: None): names of tags splitted by '','

    Returns:
        List[models.Card|None]: list of all cards fullfilling filtering criteria
    """
    with Session(engine) as session:
        statement = select(models.Card)
        if user_id:
            statement = statement.where(models.Card.user_id == user_id)
        if card_type_id:
            statement = statement.where(models.Card.card_type_id == card_type)
        if tags:
            for tag in tags.split(","):
                statement = statement.where(models.Tag.name == tag)
        return session.execute(statement).scalars().all()


async def get_user_by_id_or_default(user_id: int | None = None) -> models.User | None:
    """
    Get user of given ID if exists or get default user ('Anonymous') if no ID provided.

    Args:
        user_id (int|None, default: None): ID of requested user or None if default user requested

    Returns:
        model.User|None: instance of user with given ID or None if this ID does not exist
    """
    with Session(engine) as session:
        statement = (
            select(models.User).where(models.User.id == user_id)
            if user_id
            else select(models.User).where(models.User.name == "Anonymous")
        )
        return session.exec(statement).first()


async def get_card_type_by_id(card_type_id: int) -> models.CardType | None:
    """
    Get card type of given ID if exists.

    Args:
        user_id (int): ID of requested card type

    Returns:
        model.CardType|None: instance of card type with given ID or None if this ID does not exist
    """
    with Session(engine) as session:
        statement = select(models.CardType).where(models.CardType.id == card_type_id)
        return session.exec(statement).first()


async def get_user_by_name(username: str) -> models.User | None:
    """
    Get user of given name if exists.

    Args:
        user_id (str): name of requested user

    Returns:
        model.User|None: instance of user type with given name or None if this name does not exist
    """
    with Session(engine) as session:
        statement = select(models.User).where(models.User.name == username)
        return session.exec(statement).first()


async def get_card_by_id(card_id: int) -> models.Card | None:
    """
    Get card of given ID if exists.

    Args:
        user_id (int): ID of requested card

    Returns:
        model.Card|None: instance of card with given ID or None if this ID does not exist
    """
    with Session(engine) as session:
        statement = select(models.Card).where(models.Card.id == card_id)
        return session.exec(statement).first()


async def save_into_db(instance: SQLModel) -> SQLModel:
    """
    Save instance into database or raise IOError.

    Args:
        instance (SQLModel): instance of child class of SQLModel,
                        which contains data for saving into database

    Returns:
        SQLModel: Same instance of SQLModel but updated (with ID)

    Raises:
        IOError: if cannot save data into database
    """
    with Session(engine) as session:
        try:
            session.add(instance)
            session.commit()
        except Exception as e:
            session.rollback()
            raise IOError("Database operation failed!")
        session.refresh(instance)
        return instance


async def delete_id_db(instance: SQLModel):
    """
    Delete instance from database or raise IOError.

    Args:
        instance (SQLModel): instance of child class of SQLModel,
                        which should be deleted from database

    Raises:
        IOError: if cannot delete instance from database
    """
    with Session(engine) as session:
        try:
            session.delete(instance)
            session.commit()
        except Exception as e:
            session.rollback()
            raise IOError("Database operation failed!")


async def connect_tags_with_card(tags: List[models.Tag], card_id: int):
    """
    Save new tags into database
    and create new record to relationship table of tag and card.
    or raise IOError.

    Args:
        tags: (List[models.Tag]): list of tag instances
        card_id (int): ID of card, which should be connected with these tags

    Raises:
        IOError: if cannot save data into database
    """
    with Session(engine) as session:
        for tag in tags:
            logger.warning(f"tag {tag}")
            statement = select(models.Tag).where(models.Tag.name == tag.name)
            tag_instance = session.exec(statement).first()
            if not tag_instance:
                tag_instance = await save_into_db(
                    models.Tag(name=tag.name, description=tag.description)
                )
            await save_into_db(
                models.CardTagRelationship(card_id=card_id, tag_id=tag_instance.id)
            )
