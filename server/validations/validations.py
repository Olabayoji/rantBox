from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from routers.types.custom_types import GenderEnum


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, title="Username")
    password: str = Field(min_length=8, max_length=20, title="Password")
    email: EmailStr = Field(title="Email")
    # gender: GenderEnum

    class Config:
        orm_mode = True


class GetUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    date_created: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class ResetPasswordRequest(BaseModel):
    new_password: str = Field(min_length=8, max_length=20, title="Password")
    new_password_verified: str = Field(
        min_length=8, max_length=20, title="Password verified"
    )


class GetPostResponse(BaseModel):
    id: int
    title: str
    content: str
    date_created: datetime
    date_updated: datetime


class CreatePostRequest(BaseModel):
    title: str = Field(min_length=3, title="Title")
    content: str = Field(min_length=3, title="Content")

    class Config:
        orm_mode = True
