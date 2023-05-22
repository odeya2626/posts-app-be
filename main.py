from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import models, database
from routers import user, post
from auth import authentication as auth
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


models.Base.metadata.create_all(bind=database.engine)
app.mount("/static", StaticFiles(directory="static"), name="static")