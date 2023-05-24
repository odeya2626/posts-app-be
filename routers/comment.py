from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from routers.schemas import CommentBase, CommentDisplay
from db.db_comment import create, get_by_post

router = APIRouter(prefix="/comment", tags=["comment"])

@router.get("/all/{post_id}")
def get_all_post_comments(post_id: int, db: Session = Depends(get_db)):
    return get_by_post(db, post_id)

@router.post("/create" ,status_code=status.HTTP_201_CREATED, response_model=CommentDisplay)
def create_comment(request: CommentBase, db: Session = Depends(get_db)):
    try:
        new_comment = create(db, request)
        return new_comment
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid data")
