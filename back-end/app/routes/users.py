from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from .. import utils, oauth2
from ..schemas import users_schemas
from ..utils import sqlQuery, createContact
from ..sql_verification import check_user
import requests

router = APIRouter(prefix='/users',tags=['Users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=users_schemas.UserOut)
def make_user(user_cred: users_schemas.UserCreate):
    if check_user(user_cred.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email aldready taken")
    user_cred.password = utils.get_password_hash(user_cred.password)
    new_user = sqlQuery("INSERT INTO users (name, username, email, password, role) VALUES (%s,%s,%s,%s,%s) RETURNING *;",(user_cred.name,user_cred.username,user_cred.email,user_cred.password,user_cred.role,))
    if not new_user['join_req']: # type: ignore
        new_user['join_req'] = [] # type: ignore
    # createContact(user_cred.email,user_cred.name.split(" ")[0])
    return new_user

@router.get('/', response_model=users_schemas.UserOut)
def get_user(tokenData = Depends(oauth2.get_current_user)):
    user = sqlQuery("SELECT * FROM users WHERE user_id = %s;",(tokenData.id,))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Try loging in again')
    if not user['join_req']:  # type: ignore
        user['join_req'] = []  # type: ignore
    return user

@router.put('/', response_model=users_schemas.UserOut)
def update_user(user_cred: users_schemas.UserCreate, tokenData = Depends(oauth2.get_current_user)):
    if check_user(user_cred.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email aldready taken")
    user_cred.password = utils.get_password_hash(user_cred.password)
    new_user = sqlQuery("UPDATE users SET name = %s, username = %s, email = %s, password = %s, role = %s WHERE user_id = %s RETURNING *;",(user_cred.name,user_cred.username,user_cred.email,user_cred.password,user_cred.role,tokenData.id,))
    return new_user

@router.delete('/',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(tokenData = Depends(oauth2.get_current_user)):
    del_user = sqlQuery("DELETE FROM users WHERE user_id = %s RETURNING *;", (tokenData.id,))
    if not del_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No user deleted")