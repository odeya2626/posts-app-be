from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User
from routers.schemas import UserBase, UserDisplay
from db.db_user import create_user
import sys
sys.path.append(".")


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserDisplay )
def register(request: UserBase, db: Session = Depends(get_db)):
    print(request)
    try:
        new_user = create_user(db, request)
        return new_user
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid data")
    
