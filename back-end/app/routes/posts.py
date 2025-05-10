from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from .. import utils, oauth2
from ..schemas import posts_schemas


router = APIRouter(prefix="/posts",tags=['Posts'])

@router.get("/")
def hello():
    return {'message':'hello'}
