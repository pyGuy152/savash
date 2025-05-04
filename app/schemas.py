from pydantic import BaseModel, EmailStr

class LoginInput(BaseModel):
    username: str
    password: str

class UserInput(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    role: str
    
