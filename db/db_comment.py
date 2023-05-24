
from sqlalchemy.orm import Session
from db.models import Comment
from routers.schemas import CommentBase
from fastapi import HTTPException, status
from datetime import datetime

def create(db:Session, request: CommentBase):
    try:
        new_comment = Comment(
            text=request.text, post_id=request.post_id, username=request.username, timestamp= datetime.now()
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid data")
        
def get_by_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()
