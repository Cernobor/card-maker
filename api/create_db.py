"""
Script for reinitializing of database.
This script can be used just for debugging purposes!
"""

import json
import os

from cardmaker import models
from cardmaker.logger import setup_logger
from sqlmodel import Session, SQLModel, create_engine

engine = create_engine(os.getenv("DATABASE_URL"))
logger = setup_logger("my_logger", "app.log")


def save_card_types(card_types: list):
    """
    Save card types and card sizes into database.

    Args:
        card_types (list): list of dictionaries
    """
    with Session(engine) as session:
        for card_type in card_types:
            card_type_instance = models.CardType(name=card_type["name"])
            try:
                session.add(card_type_instance)
            except Exception as e:
                session.rollback()
                logger.error(f"Cannot save card type {card_type["name"]} into db. {e}")
                return
            session.commit()
            logger.info(f"Card type {card_type["name"]} inserted into db.")
            session.refresh(card_type_instance)
            for size in card_type["sizes"]:
                size_instance = models.Size(
                    name=size["name"], width=size["width"], height=size["height"]
                )
                try:
                    session.add(size_instance)
                except Exception as e:
                    session.rollback()
                    logger.error(f"Cannot save size {size["name"]} into db. {e}")
                    return
                session.commit()
                logger.info(f"Card size {size["name"]} inserted into db.")
                session.refresh(size_instance)
                try:
                    session.add(
                        models.CardTypeSizeRelationship(
                            card_type_id=card_type_instance.id, size_id=size_instance.id
                        )
                    )
                except Exception as e:
                    session.rollback()
                    logger.error(
                        f"Cannot save card type size relationship into db. {e}"
                    )
                    return
                session.commit()
                logger.info(f"Card type size relationship inserted into db.")


def save_users(users: list):
    """
    Save default users into database.

    Args:
        users (list): list of dictionaries
    """
    with Session(engine) as session:
        for user in users:
            try:
                session.add(models.User(name=user["name"]))
            except Exception as e:
                session.rollback()
                logger.error(f"Cannot save user {user["name"]} into db. {e}")
                return
            session.commit()
            logger.info(f"User {user["name"]} inserted into db.")


def save_tags(tags: list):
    """
    Save default tags into database.

    Args:
        tags (list): list of dictionaries
    """
    with Session(engine) as session:
        for tag in tags:
            try:
                session.add(models.Tag(name=tag["name"], visible=tag["visible"]))
            except Exception as e:
                session.rollback()
                logger.error(f"Cannot save tag {tag["name"]} into db. {e}")
                return
            session.commit()
            logger.info(f"Tag {tag["name"]} inserted into db.")


def json_to_db(json_path: str) -> list:
    """
    Read json data and save them into database.

    Args:
        json_path (str): path to the json file
    """
    with open(json_path, "r") as json_file:
        data = json.load(json_file)

    if "card_types" in data.keys():
        save_card_types(data["card_types"])

    if "users" in data.keys():
        save_users(data["users"])

    if "tags" in data.keys():
        save_tags(data["tags"])


def create_db():
    """
    Reinitialize database - drop all tables and create new tables
    This is just for debugging purposes! It will be removed.
    """
    SQLModel.metadata.drop_all(engine)
    logger.warning(f"Database dropped")
    SQLModel.metadata.create_all(engine)
    logger.info(f"Database successfully initialized")
    json_to_db("initial_data.json")
