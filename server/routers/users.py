from fastapi import APIRouter, HTTPException, status
from models import User
from fastapi import status
from validations.validations import (
    CreateUserRequest,
    GetUserResponse,
)
from global_context.context import (
    hash_password,
    db_dependency,
    user_dependency,
)


user_router = APIRouter()


# get all users
@user_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[GetUserResponse],
    tags=["users"],
)
async def get_users(db: db_dependency, user: user_dependency):

    users = db.query(User).all()
    return users


# create a new user
@user_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
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
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return
