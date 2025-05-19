from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from .. import oauth2
from ..schemas import assignments_schemas
from ..utils import sqlQuery
import random

router = APIRouter(prefix='/classes/{code}/assignments/{id}/submit',tags=['Submit'])

def userInClass(id,code):
    x = sqlQuery("SELECT * FROM user_class WHERE user_id = %s AND code = %s;",(id,code,))
    if not x or x == None:
        return False
    return True

@router.get("/")
def get_submissions():
    return

