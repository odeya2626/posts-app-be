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
    used_username = db.query(User).filter(User.username == request.username).first()
    if used_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    validate_email = db.query(User).filter(User.email == request.email).first()
    if not isvalidEmail(request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
        )
    if validate_email:
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
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    print("userget", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )
    return user


def update_user_model(db: Session, request: UserBase, user: User):
    print("user", user)
    if request.username != user.username:
        used_username = db.query(User).filter(User.username == request.username).first()
        if used_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username {request.username} already in use",
            )
        user.username = request.username
    if request.email != user.email:
        if not isvalidEmail(request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
            )
        used_email = db.query(User).filter(User.email == request.email).first()
        if used_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {request.email} already in use",
            )
        user.email = request.email
    if request.profile_img != user.profile_img:
        user.profile_img = request.profile_img
    updated_user = User(
        username=user.username,
        email=user.email,
        profile_img=user.profile_img,
    )

    db.commit()
    db.refresh(user)
    return updated_user
