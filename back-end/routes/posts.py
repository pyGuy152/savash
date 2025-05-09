from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from .. import schemas, utils, oauth2


router = APIRouter(prefix="/posts",tags=['Posts'])

