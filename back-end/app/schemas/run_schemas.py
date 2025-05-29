from typing import List, Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class Testcases(BaseModel):
    inputs: List[List[str]]
    outputs: List[str]
