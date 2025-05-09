from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class ClassMake(BaseModel):
    name: str

class ClassBase(BaseModel):
    code: int

class ClassOut(ClassBase):
    name: str
    created_at : datetime

class ClassUsers(ClassBase):
    email: EmailStr

class DelClass(ClassBase):
    pass

class UpdateClass(ClassBase):
    name: str

class JoinClass(ClassBase):
    pass
