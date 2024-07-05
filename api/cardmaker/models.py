"""
ORM models for 'Cardmaker' database and models for fastapi endpoints.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """
    Author of the card.
    Each Card instance has foreign key to User
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class CardTypeSizeRelationship(SQLModel, table=True):
    """
    Link model for CardType and Size.
    """

    __tablename__ = "cards_type_size_relationship"

    card_type_id: int = Field(
        default=None, foreign_key="card_types.id", primary_key=True
    )
    size_id: int = Field(default=None, foreign_key="sizes.id", primary_key=True)


class Size(SQLModel, table=True):
    """
    Defined sizes of particular card types.
    width and height are defined in px.
    """

    __tablename__ = "sizes"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    width: int
    height: int

    card_types: list["CardType"] = Relationship(
        back_populates="sizes", link_model=CardTypeSizeRelationship
    )


class CardType(SQLModel, table=True):
    """
    Type of card, which means for example Location or Magical item.
    Each Card has foreign key to CardType.
    """

    __tablename__ = "card_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    sizes: list[Size] = Relationship(
        back_populates="card_types", link_model=CardTypeSizeRelationship
    )


class CardTagRelationship(SQLModel, table=True):
    """
    Link model for Card and Tag models.
    """

    __tablename__ = "cards_tags_relationship"

    card_id: int = Field(default=None, foreign_key="cards.id", primary_key=True)
    tag_id: int = Field(default=None, foreign_key="tags.id", primary_key=True)


class Card(SQLModel, table=True):
    """
    Main item of the app.
    Each Card instance has author (User) and type (CardType).
    """

    __tablename__ = "cards"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    fluff: Optional[str]
    effect: Optional[str]
    user_id: int = Field(foreign_key="users.id")
    card_type_id: int = Field(foreign_key="card_types.id")

    tags: list["Tag"] = Relationship(
        back_populates="cards", link_model=CardTagRelationship
    )


class Tag(SQLModel, table=True):
    """
    Tag, which can be attached to any Card instance.
    Tag can be anything, for example year of creation
    of something, which can help with filtering.
    """

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    visible: bool

    cards: list[Card] = Relationship(
        back_populates="tags", link_model=CardTagRelationship
    )
