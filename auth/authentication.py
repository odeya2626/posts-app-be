from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from db.database import get_db
from db.models import User
from db.db_user import verify
from auth.oauth import create_access_token



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(request: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request["username"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not  verify(user.password, request["password"]):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    access_token = create_access_token(data={"username": user.username})

    return {"access_token": access_token, "token_type": "bearer", "username": user.username, "user_id": user.id}