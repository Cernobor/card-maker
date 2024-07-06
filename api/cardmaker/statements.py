"""
Functions for executing SQL statements.
"""

from typing import List
import os

from . import models
from sqlmodel import Session, select, create_engine, SQLModel

engine = create_engine(os.getenv("DATABASE_URL"))

async def get_users() -> List[models.User|None]:
    with Session(engine) as session:
        statement = select(models.User)
        return session.execute(statement).scalars().all()


async def get_card_types() -> List[models.CardType|None]:
    with Session(engine) as session:
        statement = select(models.CardType)
        return session.execute(statement).scalars().all()


async def get_tags() -> List[models.Tag|None]:
    with Session(engine) as session:
        statement = select(models.Tag)
        return session.execute(statement).scalars().all()


async def get_filtered_cards(
    user: int|None = None,
    card_type: int|None = None,
    tags: str|None = None,
) -> List[models.Card|None]:
    with Session(engine) as session:
        statement = select(models.Card)
        if user:
            statement = statement.where(models.Card.user_id == user)
        if card_type:
            statement = statement.where(models.Card.card_type_id == card_type)
        if tags:
            for tag in tags.split(","):
                statement = statement.where(models.Tag.name == tag)
        return session.execute(statement).scalars().all()


async def get_user_by_id_or_default(user_id: int = None) -> models.User|None:
    with Session(engine) as session:
        statement = (
            select(models.User).where(models.User.id == user_id)
            if user_id
            else select(models.User).where(models.User.name == "Anonymous")
        )
        return session.exec(statement).first()


async def get_card_type_by_id(card_type_id: int) -> models.CardType|None:
    with Session(engine) as session:
        statement = select(models.CardType).where(
            models.CardType.id == card_type_id
        )
        return session.exec(statement).first()


async def get_user_by_name(username: str) -> models.User|None:
    with Session(engine) as session:
        statement = select(models.User).where(
            models.User.name == username
        )
        return session.exec(statement).first()



async def get_card_by_id(card_id: int) -> models.Card|None:
    with Session(engine) as session:
        statement = select(models.Card).where(
            models.Card.id == card_id
        )
        return session.exec(statement).first()


async def save_into_db(instance: SQLModel) -> SQLModel:
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
    with Session(engine) as session:
        try:
            session.delete(instance)
            session.commit()
        except Exception as e:
            session.rollback()
            raise IOError("Database operation failed!")


async def connect_tags_with_card(tags: List[models.Tag], card_id: int):
    with Session(engine) as session:
        for tag in tags:
            statement = select(models.Tag).where(models.Tag.name == tag.name)
            tag_instance = session.exec(statement).first()
            if not tag_instance:
                new_tag = await save_into_db(models.Tag(name=tag.name, visible=tag.visible))

            save_into_db(models.CardTagRelationship(
                card_id=card_id, tag_id=new_tag.id
            ))