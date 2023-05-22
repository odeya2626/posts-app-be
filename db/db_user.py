from routers.schemas import UserBase
from sqlalchemy.orm import Session
from db.models import User
from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def bcrypt(password: str)->str:
    return pwd_context.hash(password)
def verify(hashed_password:str, plain_password: str)->bool:
    return pwd_context.verify(hashed_password, plain_password)

def create_user(db: Session, request: UserBase):
    validate_email = db.query(User).filter(User.email == request.email).first()
    if validate_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = User(
        username=request.username, email=request.email, password=bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
    return user