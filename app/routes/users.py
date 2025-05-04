from fastapi import APIRouter
from .. import schemas

router = APIRouter(prefix='/users',tags=['Users'])

@router.post('/')
def get_users(user_cred: schemas.UserInput):
    return {'data':user_cred}