from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class AssignmentBase(BaseModel):
    title: str
    description: str
    due_date: datetime
    created_at: datetime

class AssignmentOut(BaseModel):
    assignment_id: int
    title: str
    directions: str
    due_date: datetime
    created_at: datetime

class WrittenAssignment(AssignmentBase):
    pass

class MCQAssignment(AssignmentBase):
    questions: list
    choices: list
    correct_answer: list

class FRQAssignment(AssignmentBase):
    questions: list

class TFQAssignment(AssignmentBase):
    questions: list
    correct_answer: list

class CodingAssignment(AssignmentBase):
    test_case_input : list
    test_case_output : list

class UpdateAssignment(AssignmentBase):
    assignment_id: int

class DeleteAssignment(BaseModel):
    assignment_id: int