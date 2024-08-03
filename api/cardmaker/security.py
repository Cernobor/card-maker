"""
Authorization utilities
"""

import os
import secrets
from datetime import datetime
from typing import Tuple

import bcrypt
import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBearer

from . import models
from .database import CardMakerDatabase
from .logger import Logger

logger = Logger.get_instance()
database = CardMakerDatabase()

SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")
ALGORITHM = "HS256"


http_basic = HTTPBasic()


class JWTBearer(HTTPBearer):
    """
    JWT token checker.
    Override '__call__' method to make the class callable in endpoints.
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        token = await super(JWTBearer, self).__call__(request)
        if token:
            if token.scheme != "Bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication scheme!"
                )
            user = await verify_jwt(token)
            if not user:
                raise HTTPException(
                    status_code=401, detail="Invalid or expired token!"
                )
            logger.debug(token.credentials)
            return token.credentials
        else:
            raise HTTPException(
                status_code=401, detail="Invalid authorization code!"
            )


def hash_password(password: str, salt: bytes | None = None) -> Tuple[bytes]:
    """
    Has password with salt,

    Args:
        password (str): plain text password
        salt (bytes|None, default: None):
                salt should be provided for existing user,
                if salt set to None, salt will be generated

    Returns:
        bytes: hashed password
        bytes: salt
    """
    if not salt:
        salt = bcrypt.gensalt()
    return bcrypt.hashpw(str.encode(password), salt), salt


def verify_api_key(api_key: str) -> bool | None:
    """
    Verify if provided api key is the same as reference api key.

    Args:
        api_key (str): token used to allow user be registrated

    Returns:
        bool|None: if api key is correct
                    (None if reference api key does not exist)
    """
    if not API_KEY:
        logger.error("Cannot obtain api key!")
        return
    return secrets.compare_digest(api_key, API_KEY)


def create_access_token(user: models.User, expiration: datetime) -> str | None:
    """
    Generate JWT token for authentication.

    Args:
        user (models.User): user object with username, password etc.
        expiration (datetime): date of token expiration

    Returns:
        str|None: JWT token (None if secred key does not exist)
    """
    to_encode = user.model_dump()
    to_encode.update({"exp": expiration})
    to_encode.pop("salt")
    logger.debug(to_encode)
    if not SECRET_KEY:
        logger.error("Cannot obtain secret key!")
        return
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate(username: str, password: str):
    """
    Verify if provided username and password are correct.

    Args:
        user (models.User): user object with username, password etc.
        expiration (datetime): date of token expiration

    Returns:
        models.User|None: db user object
    """
    user = await database.get_user_by_name(username)
    if not user:
        logger.debug(f"{username} not in db")
        return
    hashed_password, _ = hash_password(password, user.salt)
    if not secrets.compare_digest(
        hashed_password, str.encode(user.hashed_password)
    ):
        logger.debug(f"{hashed_password} is not same as {user.hashed_password}")
        return
    return user


async def verify_jwt(token: str):
    """
    Verify if provided JWT token is correct and returns user object.

    Args:
        token (str): JWT token

    Returns:
        models.User|None: db user object
    """
    if not SECRET_KEY:
        logger.error("Cannot obtain secret key!")
        return
    try:
        payload = jwt.decode(
            token.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        logger.debug(payload)
        username = payload["username"]
        if not username:
            return
        user = await database.get_user_by_name(username)
        logger.debug(user)
        if not user:
            return
    except Exception as e:
        logger.info(e)
        return
    return user
