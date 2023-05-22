from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User
from routers.schemas import Userbase, UserDisplay
from db.db_user import create_user


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserDisplay)
def register(request: Userbase, db: Session = Depends(get_db)):
    return create_user(db, request)
