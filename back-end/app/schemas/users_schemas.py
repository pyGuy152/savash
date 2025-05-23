from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    role: UserRole

class UserOut(BaseModel):
    username: str
    email: EmailStr
    role: str
    join_req: list
    class config:
        orm_mode = True
