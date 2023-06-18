import os

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://icuafboo:dxh8xFRwo3_MfMfx4JOLJwnmQ0R9Rnmb@lucky.db.elephantsql.com/icuafboo"
database_url = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
