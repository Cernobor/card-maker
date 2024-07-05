from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """
    TODO docstring
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class CardTypeSizeRelationship(SQLModel, table=True):
    """
    TODO docstring
    """

    __tablename__ = "cards_type_size_relationship"

    card_type_id: int = Field(
        default=None, foreign_key="card_types.id", primary_key=True
    )
    size_id: int = Field(default=None, foreign_key="sizes.id", primary_key=True)


class Size(SQLModel, table=True):
    """
    TODO docstring
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
    TODO docstring
    """

    __tablename__ = "card_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    sizes: list[Size] = Relationship(
        back_populates="card_types", link_model=CardTypeSizeRelationship
    )


class CardTagRelationship(SQLModel, table=True):
    """
    TODO docstring
    """

    __tablename__ = "cards_tags_relationship"

    card_id: int = Field(default=None, foreign_key="cards.id", primary_key=True)
    tag_id: int = Field(default=None, foreign_key="tags.id", primary_key=True)


class Card(SQLModel, table=True):
    """
    TODO docstring
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
    TODO docstring
    """

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    visible: bool

    cards: list[Card] = Relationship(
        back_populates="tags", link_model=CardTagRelationship
    )
