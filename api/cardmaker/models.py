from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    TODO docstring
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Tag(SQLModel, table=True):
    """
    TODO docstring
    """

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    visible: bool


class CardType(SQLModel, table=True):
    """
    TODO docstring
    """

    __tablename__ = "card_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    width: int
    height: int
    strict_look: bool


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


class CardTagRelationship(SQLModel):
    """
    TODO docstring
    """

    __tablename__ = "cards_tags_relationship"

    id: Optional[int] = Field(default=None, primary_key=True)
    card_id: int = Field(foreign_key="cards.id")
    tag_id: int = Field(foreign_key="tags.id")


class Symbol(SQLModel, table=True):
    """
    TODO docstring
    """

    __tablename__ = "symbols"

    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str


class CardSymbolRelationship(SQLModel, table=True):
    """
    TODO docstring
    """

    __tablename__ = "cards_symbols_relationship"

    id: Optional[int] = Field(default=None, primary_key=True)
    card_id: int = Field(foreign_key="cards.id")
    tag_id: int = Field(foreign_key="symbols.id")
