from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class MakeGame(BaseModel):
    host_name: str
    min: Optional[int] = None