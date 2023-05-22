from fastapi import APIRouter, File, UploadFile, status, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
import os
from db.database import get_db
from db.db_post import create, get_all
from routers.schemas import PostBase, PostDisplay, UserAuth
from db.models import Post
from datetime import datetime
from typing import Optional
from auth.oauth import get_current_user



router = APIRouter(prefix="/post", tags=["post"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostDisplay)
def create_post(request:PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    if not request.img_url_type in ["absolute", "relative"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image url type")
    try:
        new_post = create(db, request)
        return new_post
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data")
    
@router.get("/all", response_model=list[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)):
    return get_all(db)

@router.post("/image")
def upload_image(image: UploadFile = File(...)):
    print(image)
    image_name:Optional[str]= image.filename
    timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
    # filename: str = os.path.join(timestamp, image_name or "")
    filename: str = f"{timestamp}_{image_name}"
    print(filename)

    path = f"static/images/{filename}"
    # os.makedirs(path, exist_ok=True)
    with open (path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"filename": path}
