"""
ORM models for 'Cardmaker' database and models for fastapi endpoints.
"""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Token(SQLModel):
    """
    JWT token
    """

    access_token: str
    token_type: str


class UserBase(SQLModel):
    """
    Base model of author of the card.
    """

    username: str


class UserCreate(UserBase):
    """
    User model for 'create_user' POST method.
    """

    password: str


class UserPublic(UserBase):
    """
    User model for 'get_users' GET method.
    """

    id: int


class User(UserBase, table=True):
    """
    Each Card instance has foreign key to User
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: Optional[str]
    anonymous: bool


class CardType(SQLModel, table=True):
    """
    Type of card, which means for example Location or Magical item.
    Each Card has foreign key to CardType.
    """

    __tablename__ = "card_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class CardTagRelationship(SQLModel, table=True):
    """
    Link model for Card and Tag models.
    """

    __tablename__ = "cards_tags_relationship"

    card_id: int = Field(default=None, foreign_key="cards.id", primary_key=True)
    tag_id: int = Field(default=None, foreign_key="tags.id", primary_key=True)


class TagBase(SQLModel):
    """
    Base model for tag.
    Tag can be anything, for example year of creation
    of something, which can help with filtering.
    """

    name: str
    description: Optional[str]


class Tag(TagBase, table=True):
    """
    Tag, which can be attached to any Card instance.
    """

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)

    cards: List["Card"] = Relationship(
        back_populates="tags", link_model=CardTagRelationship
    )


class CardBase(SQLModel):
    """
    Base model for card: main item of the app.
    """

    name: str
    fluff: Optional[str]
    effect: Optional[str]
    in_set: bool
    set_name: Optional[str]


class CardCreate(CardBase):
    """
    Card model for 'create_card' POST method.
    """

    tag_list: List[TagBase | None]
    user_id: int
    card_type_id: int


class CardGet(CardCreate):
    """
    Card model for 'get_cards' and
    'get_card_by_id' GET method.
    """

    id: int


class CardUpdate(CardBase):
    """
    Card model for 'update_card' PUT method.
    """

    tag_list: List[TagBase | None]


class Card(CardBase, table=True):
    """
    Each Card instance has author (User) and type (CardType).
    """

    __tablename__ = "cards"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    card_type_id: int = Field(foreign_key="card_types.id")

    tags: List[Tag] = Relationship(
        back_populates="cards", link_model=CardTagRelationship
    )
