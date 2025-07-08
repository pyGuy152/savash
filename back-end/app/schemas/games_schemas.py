from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class MakeGame(BaseModel):
    days: Optional[int] = 0
    hours: Optional[int] = 0
    min: Optional[int] = 0
    assignment_id: Optional[int] = None