from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from global_fn.fn import get_db
from models import User
from fastapi import status

from validations.validations import CreateUserRequest, GetUserResponse

router = APIRouter()


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=list[GetUserResponse],
)
async def get_users(db: Annotated[Session, Depends(get_db)]):
    users = db.query(User).all()
    return users


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: CreateUserRequest, db: Annotated[Session, Depends(get_db)]):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    print(user.model_dump())
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
