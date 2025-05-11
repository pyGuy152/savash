from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class AssignmentTypes(str, Enum):
    WRITTEN = 'Written'
    MCQ = 'MCQ'
    FRQ = 'FRQ'
    TFQ = 'TFQ'
    CODING = 'Coding'

class AssignmentOut(BaseModel):
    assignment_id: int
    title: str
    description: str
    due_date: datetime
    created_at: datetime

class MakeAssignment(BaseModel):
    title: str
    description: str
    due_date: datetime
    type: AssignmentTypes

class UpdateAssignment(MakeAssignment):
    assignment_id: int

class DeleteAssignment(BaseModel):
    assignment_id: int