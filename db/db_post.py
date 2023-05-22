from sqlalchemy.orm import Session
from db.models import Post
from routers.schemas import PostBase, PostDisplay
from datetime import datetime

def create(db: Session, request: PostBase):
    new_post = Post(
        img_url=request.img_url, img_url_type=request.img_url_type, caption=request.caption, creator_id=request.creator_id, timestamp=datetime.now(),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post == PostDisplay, "new_post", new_post)
    return new_post

def get_all(db: Session):
    return db.query(Post).all()
