import os
import shutil
from datetime import datetime
from typing import Optional

import cloudinary
from auth.oauth import get_current_user
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from db.database import get_db
from db.db_post import create, delete, get_all
from db.models import Post, User
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import ValidationError
from routers.schemas import PostBase, PostDisplay, UserAuth
from sqlalchemy.orm import Session

load_dotenv()
router = APIRouter(prefix="/post", tags=["post"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostDisplay)
def create_post(
    request: PostBase,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    print("current user id", current_user.id)
    try:
        PostBase(**request.dict())
        creator_username = db.query(User).filter(User.id == request.creator_id).first()
        if not creator_username or not creator_username.username:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
    except ValidationError as e:
        print("e", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )
    if not request.img_url_type in ["absolute", "relative"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image url type"
        )
    try:
        new_post = create(db, request)
        return new_post
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )


@router.get("/all", response_model=list[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)):
    return get_all(db)


@router.post("/image")
def upload_image(
    image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)
):
    print("image", image)
    image_name: Optional[str] = image.filename
    timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
    # filename: str = os.path.join(timestamp, image_name or "")
    filename: str = f"{timestamp}_{image_name}"
    print(filename)

    # path = f"static/images/{filename}"
    # # os.makedirs(path, exist_ok=True)
    # with open(path, "wb") as buffer:
    #     shutil.copyfileobj(image.file, buffer)
    # return {"filename": path}
    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("API_KEY"),
        api_secret=os.getenv("API_SECRET"),
        secure=True,
    )
    upload_result = upload(image.file, folder="posts-app", public_id=filename)

    url, options = cloudinary_url(
        upload_result["public_id"],
        format=upload_result["format"],
        width=upload_result["width"],
        height=upload_result["height"],
        crop="fill",
    )

    return {"filename": url}


@router.delete("/delete/{id}")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    return delete(id, db, current_user_id=current_user.id)
