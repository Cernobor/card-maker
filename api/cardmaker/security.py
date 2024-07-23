"""
Authorization utilities
"""

import os
import secrets
from datetime import datetime
from typing import Tuple

import jwt
import bcrypt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer

from . import models, statements
from .logger import Logger

logger = Logger.get_instance()
SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")
# just for development purposes
# this lines will be removed and new secret key will be generated
SECRET_KEY = "6de9b7c10564fb4794c13a2c127b5a00e21259cd56df440aad5199dae182966b"
API_KEY = "7d9e46b9-c8d9-429b-88b0-8de20a4268a0"
ALGORITHM = "HS256"


http_basic = HTTPBasic()


class JWTBearer(HTTPBearer):
    """
    TODO docstring
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


def hash_password(password: str, salt: str|None = None) -> Tuple[bytes]:
    """
    TODO docstring
    """
    if not salt:
        salt = bcrypt.gensalt()
    return bcrypt.hashpw(str.encode(password), salt), salt


def verify_api_key(api_key: str):
    """
    TODO docstring
    """
    if not API_KEY:
        logger.error("Cannot obtain api key!")
        return
    return secrets.compare_digest(
        api_key, API_KEY
    )
    

def create_access_token(user: models.User, expiration: datetime):
    """
    TODO docstring
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
    TODO docstring
    """
    user = await statements.get_user_by_name(username)
    if not user:
        logger.debug(f"{username} not in db")
        return
    hashed_password, _ = hash_password(password, user.salt);
    if not secrets.compare_digest(
        hashed_password, str.encode(user.hashed_password)
    ):
        logger.debug(
            f"{hashed_password} is not same as {user.hashed_password}"
        )
        return
    return user


async def verify_jwt(token: str):
    """
    TODO docstring
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
        user = await statements.get_user_by_name(username)
        logger.debug(user)
        if not user:
            return
    except Exception as e:
        logger.info(e)
        return
    return user
