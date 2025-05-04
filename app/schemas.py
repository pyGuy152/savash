from pydantic import BaseModel, EmailStr

class LoginInput(BaseModel):
    email: str
    password: str

class UserInput(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    role: str
    
