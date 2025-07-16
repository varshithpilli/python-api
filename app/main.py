from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from . routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

load_dotenv()

host = os.getenv("HOST")
database = os.getenv("DATABASE")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connected successfully")
        break
    except Exception as error:
        print(f"Conncetion to DB failed: {error}")
        time.sleep(2)

# SQLAlchemy test
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": "success",
            "data": posts}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def get_message():
    return {"message": "Landed successful"}