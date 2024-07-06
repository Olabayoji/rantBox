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
    user_dependency,
    pwd_context,
)
from models import User
from fastapi import status
from validations.validations import (
    CreateUserRequest,
    GetUserResponse,
    ResetPasswordRequest,
    Token,
)


router = APIRouter()


# login
@router.post(
    "/token", status_code=status.HTTP_200_OK, response_model=Token, tags=["auth"]
)
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


# Reset Password
@router.post("/reset-password", status_code=status.HTTP_201_CREATED, tags=["auth"])
async def resetPassword(
    user: user_dependency, db: db_dependency, form_data: ResetPasswordRequest
):

    # check if new password and new password verified are the same
    if form_data.new_password != form_data.new_password_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    # check if the user exists
    user_data = db.query(User).filter(User.id == user["user_id"]).first()
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found",
        )

    # check if the new password is the same as the old password
    if pwd_context.verify(form_data.new_password, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the old password",
        )

    # if all checks pass, hash the new password
    hashed_password = hash_password(form_data.new_password)

    # update the password
    user_data.password = hashed_password
    db.commit()
    db.refresh(user_data)

    return
