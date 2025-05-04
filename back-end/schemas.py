from typing import Optional
from pydantic import BaseModel, EmailStr

class LoginInput(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    role: str 

class UserOut(BaseModel):
    username: str
    email: EmailStr
    role: str
    class config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None