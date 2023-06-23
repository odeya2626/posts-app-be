from datetime import datetime

from pydantic import BaseModel

# from enum import Enum


class UserBase(BaseModel):
    username: str
    email: str
    password: str = None
    profile_img: str = None

    class Config:
        orm_mode = True


class UserDisplay(BaseModel):
    username: str
    email: str
    password: str
    profile_img: str = None

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    img_url: str
    img_url_type: str
    caption: str
    creator_id: int

    class Config:
        orm_mode = True


class CommentDisplay(BaseModel):
    id: int
    text: str
    username: str

    class Config:
        orm_mode = True


# for PostDisplay
class User(BaseModel):
    username: str
    profile_img: str = None

    class Config:
        orm_mode = True


class PostDisplay(BaseModel):
    id: int
    img_url: str
    img_url_type: str
    caption: str
    creator_id: int
    timestamp: datetime
    user: User
    comments: list[CommentDisplay]

    # user: User
    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    id: int
    username: str
    email: str
    profile_img: str = None


class CommentBase(BaseModel):
    text: str
    username: str
    post_id: int

    class Config:
        orm_mode = True
