from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from .users_schemas import UserRole

class ClassMake(BaseModel):
    name: str

class ClassOut(BaseModel):
    code: int
    name: str
    created_at : datetime

class ClassUsers(BaseModel):
    email: EmailStr

class UpdateClass(BaseModel):
    name: str

class UsersInClass(BaseModel):
    name: str
    username: str
    email: EmailStr
    role: UserRole