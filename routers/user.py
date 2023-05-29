import sys

from db.database import get_db
from db.db_user import create_user
from db.models import User
from fastapi import APIRouter, Depends, HTTPException, status
from routers.schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session

sys.path.append(".")


router = APIRouter(prefix="/user", tags=["user"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserDisplay
)
def register(request: UserBase, db: Session = Depends(get_db)):
    print(request)
    new_user = create_user(db, request)
    return new_user
