"""
Script for reinitializing of database.
This script will be used just in development.
"""

import json
import os

from cardmaker import models
from cardmaker.logger import Logger
from sqlmodel import Session, SQLModel, create_engine

logger = Logger.get_instance()
engine = create_engine(os.getenv("DATABASE_URL"))
logger.info("Engine created")


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
                session.add(models.Tag(name=tag["name"], description=tag["description"]))
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
    #SQLModel.metadata.drop_all(engine)
    logger.warning(f"Database dropped")
    #SQLModel.metadata.create_all(engine)
    logger.info(f"Database successfully initialized")
    json_to_db("initial_data.json")
