from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class LoginInput(BaseModel):
    email: str
    password: str


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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

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

class AssignmentOut(BaseModel):
    title: str
    description: str
    due_date: datetime
    created_at: datetime