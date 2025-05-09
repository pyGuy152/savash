from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime


class AssignmentOut(BaseModel):
    assignment_id: int
    title: str
    description: str
    due_date: datetime
    created_at: datetime

class MakeAssignment(BaseModel):
    code: int
    title: str
    description: str
    due_date: datetime

class UpdateAssignment(MakeAssignment):
    assignment_id: int

class DeleteAssignment(BaseModel):
    code: int
    assignment_id: int