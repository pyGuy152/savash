from fastapi import APIRouter, HTTPException, status
from .. import utils, oauth2
from ..schemas import auth_schemas
from ..utils import sqlQuery

router = APIRouter(tags=['Auth'])

@router.post("/login", response_model=auth_schemas.Token)
def login(user_cred: auth_schemas.LoginInput):
    hashed_pass = sqlQuery("SELECT * FROM users WHERE email = %s;",(user_cred.email,))
    if not hashed_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    if utils.verify_password(user_cred.password,hashed_pass['password']):   # type: ignore
        access_token = oauth2.create_access_token(data = {"user_id": hashed_pass['user_id']})  # type: ignore
        return {'access_token':access_token, 'token_type':"bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")

