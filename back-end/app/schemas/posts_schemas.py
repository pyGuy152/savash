from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class AddPost(BaseModel):
    tile : str
    description: str
