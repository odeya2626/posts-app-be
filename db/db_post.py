from datetime import datetime

from db.models import Post
from fastapi import HTTPException, status
from routers.schemas import PostBase, PostDisplay
from sqlalchemy.orm import Session


def create(db: Session, request: PostBase):
    new_post = Post(
        img_url=request.img_url,
        img_url_type=request.img_url_type,
        caption=request.caption,
        creator_id=request.creator_id,
        timestamp=datetime.now(),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post == PostDisplay, "new_post", new_post)
    return new_post


def get_all(db: Session):
    return db.query(Post).all()


def get_posts(db: Session, limit: int, page: int):
    try:
        result = (
            db.query(Post)
            .order_by(Post.timestamp.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        print("result", result)
        return result

    except Exception as e:
        print("e", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )


def delete(id: int, db: Session, current_user_id: int):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.creator_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own posts",
        )
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}
