import re

from db.models import User
from fastapi import HTTPException, status
from passlib.context import CryptContext
from routers.schemas import UserBase
from sqlalchemy.orm import Session

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(password: str) -> str:
    return pwd_context.hash(password)


def verify(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def isvalidEmail(email):
    pattern = "^\S+@\S+\.\S+$"
    if re.match(pattern, email):
        return True
    return False


def create_user(db: Session, request: UserBase):
    validate_email = db.query(User).filter(User.email == request.email).first()
    if not isvalidEmail(request.email):
        print("Invalid email")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
        )
    if validate_email:
        print("Email already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_user = User(
        username=request.username,
        email=request.email,
        password=bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )
    return user
