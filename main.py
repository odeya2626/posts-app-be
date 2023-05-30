from auth import authentication
from db import database, models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import comment, post, user

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(authentication.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://posts-app-fe.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
