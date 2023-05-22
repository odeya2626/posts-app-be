from routers.schemas import Userbase
from sqlalchemy.orm import Session
from db.models import User


def create_user(db: Session, request: Userbase):
    new_user = User(
        username=request.username, email=request.email, password=request.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
