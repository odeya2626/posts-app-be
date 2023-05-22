from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import models, database
from routers import user

app = FastAPI()
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


models.Base.metadata.create_all(bind=database.engine)
