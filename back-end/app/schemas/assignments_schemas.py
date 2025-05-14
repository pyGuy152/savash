from typing import Optional
from itsdangerous import NoneAlgorithm
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    points: Optional[int] = None
    due_date: Optional[datetime] = None
    created_at: datetime

class AssignmentOut(BaseModel):
    assignment_id: int
    title: str
    description: str
    questions: Optional[list] = None
    choices: Optional[list] = None
    correct_answer: Optional[list] = None
    points: Optional[int] = None
    due_date: Optional[datetime] = None
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
    input: list
    output: list


class UpdateAssignment(BaseModel):
    assignment_id: int
    title: str
    description: str
    questions: Optional[list] = None
    choices: Optional[list] = None
    correct_answer: Optional[list] = None
    points: Optional[int] = None
    due_date: Optional[datetime] = None

class DeleteAssignment(BaseModel):
    assignment_id: int

