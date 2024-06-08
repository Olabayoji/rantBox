from datetime import datetime, timedelta
import os
from database import SessionLocal
from passlib.context import CryptContext
from models import User
from jose import JWTError, jwt

from typing import Annotated

from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer


# Constants
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


# Create a password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


#
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        user_id = payload.get("user_id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
        return {"username": username, "user_id": user_id}

    except:
        raise JWTError("Could not validate credentials")


user_dependency = Annotated[dict[str, str], Depends(get_current_user)]


# function to authenticate user
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
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encode


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
