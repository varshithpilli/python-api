from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
import time
from . import models
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

load_dotenv()

host = os.getenv("HOST")
database = os.getenv("DATABASE")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

while True:
    try:
        conn = psycopg2.connect(host=host, database=database, user=user, password=password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connected successfully")
        break
    except Exception as error:
        print(f"Conncetion to DB failed: {error}")
        time.sleep(2)

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": "success",
            "data": posts}

@app.get("/")
def get_message():
    return {"message": "Landed successful"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    post_dict = post.model_dump()
    return {"message": "Create post successful",
            "data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id, ))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=404,
                            detail=f"Post with id: {id} was not found.")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id, ))
    post = cursor.fetchone()
    conn.commit()
    if post is None:
        raise HTTPException(status_code=404,
                            detail=f"Post with id: {id} was not found.")
    return

@app.put("/posts/{id}")
def update_post(id: int, response: Response, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=404,
                            detail=f"Post with id: {id} was not found.")
    return {"Message": f"Updated post with id: {id}",
            "Data": updated_post}