from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class MakeGame(BaseModel):
    days: int
    hours: int
    min: int