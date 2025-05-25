from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from .. import utils, oauth2
from ..schemas import posts_schemas
from ..utils import sqlQuery
from ..sql_verification import userInClass


router = APIRouter(prefix="/classes/{code}/posts",tags=['Posts'])

@router.get("/", response_model=List[posts_schemas.PostOut])
def get_posts(code: int, tokenData = Depends(oauth2.get_current_user)):
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User not in class')
    posts = sqlQuery('SELECT * FROM posts WHERE code = %s;',(code,),fetchALL=True)
    return posts

