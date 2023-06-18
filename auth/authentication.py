from typing import Annotated

from auth.oauth import create_access_token
from db.database import get_db
from db.db_user import verify
from db.models import User
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(tags=["auth"])


@router.post("/login")
def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )

    if not verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    access_token = create_access_token(data={"username": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
    }
