from datetime import datetime, timedelta
import os
from database import SessionLocal
from passlib.context import CryptContext
from models import User
from jose import jwt

from typing import Annotated

from fastapi import Depends

from sqlalchemy.orm import Session


# Create a password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(db: db_dependency, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = jwt.encode(
        {"sub": username, "user_id": user_id, "exp": datetime.now() + expires_delta},
        os.getenv("SECRET_KEY", "default_secret_key"),
        algorithm=os.getenv("ALGORITHM", "HS256"),
    )
    return encode


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
