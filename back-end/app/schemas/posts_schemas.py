from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class AddPost(BaseModel):
    title : str
    content: str

class PostOut(BaseModel):
    post_id: int
    user_name: str
    title: str
    content: str
    posted_at: datetime