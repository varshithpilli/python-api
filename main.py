from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import Response, status, HTTPException

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {
        "_id": 1,
        "title": "post1",
        "content": "content1",
    },
    {
        "_id": 2,
        "title": "foods",
        "content": "I like pizza",
    }
]

def get_idx(id: int):
    for idx, post in enumerate(my_posts):
        if post["_id"] == id:
            return idx
    return None

@app.get("/")
def get_message():
    return {"message": "Landing successful"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['_id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"message": "Create post successful",
            "data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    idx = get_idx(id)
    if idx is None:
        raise HTTPException(status_code=404,
                            detail=f"Post with id: {id} was not found.")
    post = my_posts[idx]
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    idx = get_idx(id)
    if idx is None:
        raise HTTPException(status_code=404,
                            detail=f"Post with id: {id} was not found.")
    my_posts.pop(idx)
    return

@app.put("/posts/{id}")
def update_post(id: int, response: Response, post: Post):
    idx = get_idx(id)
    if idx is None:
        raise HTTPException(status_code=404,
                            detail=f"Post with id: {id} was not found.")
    post_dict = post.model_dump()
    post_dict["_id"] = id
    my_posts[idx] = post_dict
    return {"Message": f"Updated post with id: {id}",
            "Data": post_dict}