from datetime import timedelta
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from global_context.context import (
    authenticate_user,
    create_access_token,
    hash_password,
    db_dependency,
)
from models import User
from fastapi import status
from validations.validations import CreateUserRequest, GetUserResponse, Token

router = APIRouter()


# get all users
@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=list[GetUserResponse],
)
async def get_users(db: db_dependency):
    users = db.query(User).all()
    return users


# create a new user
@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: CreateUserRequest, db: db_dependency):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        gender=user.gender,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# login
@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
    response: Response,
):
    user = authenticate_user(db, form_data.username, form_data.password)
    # if user does not exist, raise error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    # if user exists and password is valid, send jwt token
    access_token = create_access_token(user.username, user.id, timedelta(minutes=20))
    response.set_cookie(
        key="cookie",
        value=access_token,
        httponly=True,
        secure=bool(os.getenv("SECURE_COOKIE", False)),
    )

    return {"access_token": access_token, "token_type": "bearer"}
