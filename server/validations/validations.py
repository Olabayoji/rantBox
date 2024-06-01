from datetime import date
from pydantic import BaseModel, EmailStr, Field

from routers.types.custom_types import GenderEnum


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, title="Username")
    password: str = Field(min_length=8, max_length=20, title="Password")
    email: EmailStr = Field(title="Email")
    gender: GenderEnum

    class Config:
        orm_mode = True


class GetUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    gender: GenderEnum
    date_created: date
