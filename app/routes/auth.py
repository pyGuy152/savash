from fastapi import APIRouter
from .. import schemas

router = APIRouter(tags=['Auth'])

@router.post("/login")
def login(user_cred: schemas.LoginInput):
    return {'data':user_cred}