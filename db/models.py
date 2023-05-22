from .database import Base
from sqlalchemy import Column,DateTime ,Integer, String, Boolean, ForeignKey

from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    items = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    img_url = Column(String)
    img_url_type = Column(String)
    caption = Column(String)
    creator_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="items")