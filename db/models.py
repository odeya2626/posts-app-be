from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    profile_img = Column(String, nullable=True)

    items = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    img_url = Column(
        String,
        nullable=False,
    )
    img_url_type = Column(String, nullable=False)
    caption = Column(String, nullable=False)
    creator_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    timestamp = Column(DateTime)

    user = relationship("User", back_populates="items")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    text = Column(
        String,
        nullable=False,
    )
    username = Column(
        String,
        nullable=False,
    )
    timestamp = Column(
        DateTime,
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
    )

    post = relationship("Post", back_populates="comments")
