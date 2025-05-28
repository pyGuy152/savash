from typing import Optional, List
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
    points: Optional[int] = None
    due_date: Optional[datetime] = None
    created_at: datetime

class WrittenAssignment(AssignmentBase):
    pass

class MCQAssignment(AssignmentBase):
    questions: List[str]
    choices: List[List[str]]
    correct_answer: List[str]

class FRQAssignment(AssignmentBase):
    questions: List[str]

class TFQAssignment(AssignmentBase):
    questions: List[str]
    correct_answer: List[str]

class CodingAssignment(AssignmentBase):
    input: List[str]
    output: List[str]


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

