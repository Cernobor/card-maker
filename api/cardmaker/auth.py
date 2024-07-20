"""
Authorization
"""
from datetime import datetime
import os
import jwt

from . import models

SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = "6de9b7c10564fb4794c13a2c127b5a00e21259cd56df440aad5199dae182966b"

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
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")