import sys

sys.path.append(".")

from auth.oauth import get_current_user
from db.database import get_db
from db.db_user import create_user, update_user_model
from db.models import User
from fastapi import APIRouter, Depends, HTTPException, status
from routers.schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["user"])


@router.put("/", status_code=status.HTTP_202_ACCEPTED)
def update_user(
    request: UserBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request)
    updated_user = update_user_model(db, request, current_user)
    return updated_user


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserDisplay
)
def register(request: UserBase, db: Session = Depends(get_db)):
    new_user = create_user(db, request)
    return new_user
