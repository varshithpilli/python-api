from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostUpdate(PostBase):
    pass

class PostCreate(PostBase):
    pass

class Post(PostBase):
    created_at: datetime
    class Config:
        from_attributes = True