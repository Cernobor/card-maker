import os
from typing import List, Callable
from functools import wraps

from sqlmodel import Session, SQLModel, create_engine, select

from . import models
from .logger import Logger

logger = Logger.get_instance()


def session_wrapper(function: Callable):
    """
    Wrap method into database session.
    """

    @wraps(function)
    async def wrapper(self, *args, **kwargs):
        with Session(self.engine) as session:
            return await function(self, session, *args, **kwargs)

    return wrapper


class CardMakerDatabase:
    """
    Class for communication with database
    """

    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))

    @session_wrapper
    async def save_into_db(self, session, instance: SQLModel) -> SQLModel:
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
        try:
            session.add(instance)
            session.commit()
        except Exception as e:
            session.rollback()
            raise IOError(f"Database operation failed! {e}")
        session.refresh(instance)
        logger.info(f"Instance {instance} saved into db.")
        return instance

    @session_wrapper
    async def delete_id_db(self, session, instance: SQLModel):
        """
        Delete instance from database or raise IOError.

        Args:
            instance (SQLModel): instance of child class of SQLModel,
                            which should be deleted from database

        Raises:
            IOError: if cannot delete instance from database
        """
        try:
            session.delete(instance)
            session.commit()
        except Exception as e:
            session.rollback()
            raise IOError(f"Database operation failed! {e}")

    @session_wrapper
    async def get_users(self, session) -> List[models.UserPublic | None]:
        """
        Get all users from database.

        Returns:
            List[models.User|None]: list of all users in db
        """
        statement = select(models.User)
        return [
            models.UserPublic.model_validate(db_user)
            for db_user in session.execute(statement).scalars().all()
        ]

    @session_wrapper
    async def get_card_types(self, session) -> List[models.CardType | None]:
        """
        Get all card types from database.

        Returns:
            List[models.CardType|None]: list of all card types in db
        """
        statement = select(models.CardType)
        return session.execute(statement).scalars().all()

    @session_wrapper
    async def get_tags(self, session) -> List[models.Tag | None]:
        """
        Get all tags from database.

        Returns:
            List[models.Tag|None]: list of all tags in db
        """
        statement = select(models.Tag)
        return session.execute(statement).scalars().all()

    @session_wrapper
    async def get_filtered_cards(
        self,
        session,
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
        statement = select(models.Card)
        if user_id:
            statement = statement.where(models.Card.user_id == user_id)
        if card_type_id:
            statement = statement.where(
                models.Card.card_type_id == card_type_id
            )
        if tags:
            for tag in tags.split(","):
                statement = statement.where(models.Tag.name == tag)
        return session.execute(statement).scalars().all()

    @session_wrapper
    async def get_user_by_id_or_default(
        self,
        session,
        user_id: int | None = None,
    ) -> models.User | None:
        """
        Get user of given ID if exists
        or get default user ('Anonym')if no ID provided.

        Args:
            user_id (int|None, default: None):
                    ID of requested user
                    or None if default user requested

        Returns:
            model.User|None:
                    instance of user with given ID
                    or None if this ID does not exist
        """
        statement = (
            select(models.User).where(models.User.id == user_id)
            if user_id
            else select(models.User).where(models.User.username == "Anonym")
        )
        return session.exec(statement).first()

    @session_wrapper
    async def get_card_type_by_id(
        self, session, card_type_id: int
    ) -> models.CardType | None:
        """
        Get card type of given ID if exists.

        Args:
            user_id (int): ID of requested card type

        Returns:
            model.CardType|None:
            instance of card type with given ID
            or None if this ID does not exist
        """
        statement = select(models.CardType).where(
            models.CardType.id == card_type_id
        )
        return session.exec(statement).first()

    @session_wrapper
    async def get_user_by_name(
        self, session, username: str
    ) -> models.User | None:
        """
        Get user of given name if exists.

        Args:
            user_id (str): name of requested user

        Returns:
            model.User|None:
            instance of user type with given name
            or None if this name does not exist
        """
        statement = select(models.User).where(models.User.username == username)
        return session.exec(statement).first()

    @session_wrapper
    async def get_card_by_id(self, session, card_id: int) -> models.Card | None:
        """
        Get card of given ID if exists.

        Args:
            user_id (int): ID of requested card

        Returns:
            model.Card|None:
            instance of card with given ID
            or None if this ID does not exist
        """
        statement = select(models.Card).where(models.Card.id == card_id)
        return session.exec(statement).first()

    @session_wrapper
    async def get_tags_of_card(self, session, card_id: int) -> List[models.Tag]:
        """
        Get all tags connected to specific card.

        Args:
            card_id (int): ID of card connected to tags

        Returns:
            List[models.Tag]: list of tags of card
        """
        statement = select(models.Card).where(models.Card.id == card_id)
        return session.exec(statement).first().tag_list

    @session_wrapper
    async def get_card_tag_relationship_of_card(
        self, session, card_id: int
    ) -> List[models.CardTagRelationship]:
        """
        Select from database instance of relationship between card and tag
        based on card ID.

        Args:
            card_id (int): ID of card

        Returns:
            List[models.CardTagRelationship]:
                        list of all relationship of this card
        """
        statement = select(models.CardTagRelationship).where(
            models.CardTagRelationship.card_id == card_id
        )
        return session.exec(statement).all()

    @session_wrapper
    async def _delete_removed_tags_from_card(
        self,
        session,
        card_tag_relationship: List[models.CardTagRelationship],
        card_tags_names: List[str],
    ):
        """
        Delete relationship if tag was removed from card
        or raise IOError.

        Args:
            card_tag_relationship: (List[models.CardTagRelationship]):
                                    list of relationships
            card_tags_names (List[str]): list of names added to tag

        Raises:
            IOError: if cannot save data into database
        """
        for i in range(len(card_tag_relationship)):
            statement = select(models.Tag).where(
                models.Tag.id == card_tag_relationship[i].tag_id
            )
            tag = session.exec(statement).first()
            if (
                tag
                and tag.name not in card_tags_names
                and tag.description != "year"
            ):
                await self.delete_id_db(card_tag_relationship[i])

    @session_wrapper
    async def _save_added_tags_to_card(
        self, session, tags: List[models.Tag], card_id: int
    ):
        """
        Save tag into database if not exists,
        create new record to relationship table of tag and card if not exist,
        or raise IOError.

        Args:
            tags: (List[models.Tag]): list of tag instances
            card_id (int): ID of card, which should be connected with these tags

        Raises:
            IOError: if cannot save data into database
        """
        for tag in tags:
            statement = select(models.Tag).where(models.Tag.name == tag.name)
            tag_instance = session.exec(statement).first()
            if not tag_instance:
                tag_instance = await self.save_into_db(
                    models.Tag(name=tag.name, description=tag.description)
                )
            statement = (
                select(models.CardTagRelationship)
                .where(models.CardTagRelationship.card_id == card_id)
                .where(models.CardTagRelationship.tag_id == tag_instance.id)
            )
            if not session.exec(statement).first():
                await self.save_into_db(
                    models.CardTagRelationship(
                        card_id=card_id, tag_id=tag_instance.id
                    )
                )

    async def connect_tags_with_card(
        self, tags: List[models.Tag], card_id: int
    ):
        """
        Save tag into database if not exists,
        create new record to relationship table of tag and card if not exist,
        and delete relationship if tag was removed from card
        or raise IOError.

        Args:
            tags: (List[models.Tag]): list of tag instances
            card_id (int): ID of card, which should be connected with these tags

        Raises:
            IOError: if cannot save data into database
        """
        try:
            await self._delete_removed_tags_from_card(
                await self.get_card_tag_relationship_of_card(card_id),
                [tag.name for tag in tags],
            )
            await self._save_added_tags_to_card(tags, card_id)
        except Exception as e:
            raise (e)
