from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from routers.types.custom_types import str_20


class Base(DeclarativeBase):
    pass


# Association table for many-to-many relationship between Post and Tag
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str_20] = mapped_column(String(20))
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    date_updated: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="post", lazy="dynamic"
    )
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=post_tags, back_populates="posts"
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    date_updated: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"), index=True)

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    posts: Mapped[list["Post"]] = relationship(
        "Post", secondary=post_tags, back_populates="tags"
    )
