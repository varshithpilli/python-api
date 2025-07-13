from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def get_message():
    return {"message": "Landing successful"}

@app.get("/posts")
def get_post():
    return {"data": "Posts successful"}

@app.post("/createposts")
def create_posts(post: Post):
    return {"message": "Create posts successful",
            "data": post}