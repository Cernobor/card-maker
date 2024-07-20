"""
Authorization utilities
"""
from datetime import datetime
import os
import jwt
import secrets
from fastapi import Request, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer

from . import models, statements
from .logger import Logger

logger = Logger.get_instance()
SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = "6de9b7c10564fb4794c13a2c127b5a00e21259cd56df440aad5199dae182966b"
ALGORITHM = "HS256"


http_basic = HTTPBasic()


class JWTBearer(HTTPBearer):
    """
    TODO docstring
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self):
        token = await super(JWTBearer, self).__call__(request)
        if token:
            if token.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme!")
            if not await verify_jwt(token):
                raise HTTPException(status_code=403, detail="Invalid or expired token!")
            return token.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code!")


def hash_password(password: str):
    """
    TODO
    passlib library can be used:
    https://passlib.readthedocs.io/en/stable/
    """
    return f"hashed password {password} + salt"


def create_access_token(user: models.User, expiration: datetime):
    """
    TODO docstring
    """
    to_encode = user.model_dump()
    to_encode.update({"exp": expiration})
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
    if not secrets.compare_digest(
        auth.hash_password(password), user.hashed_password
    ):
        logger.debug(f"{hash_password(password)} is not same as {user.hashed_password}")
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return
        user = await statements.get_user_by_name(username)
        if not user:
            return
    except (InvalidTokenError, ValidationError):
        return
    return user