from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from routers.types.custom_types import GenderEnum, str_20


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str_20] = mapped_column()
    date_created: Mapped[datetime] = mapped_column(default=datetime.now)
    gender: Mapped[str_20] = mapped_column()

    def __init__(self, username: str, email: str, password: str, gender: GenderEnum):
        self.username = username
        self.email = email
        self.password = password
        self.gender = gender
