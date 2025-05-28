from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from .. import utils, oauth2
from ..schemas import posts_schemas
from ..utils import sqlQuery
from ..sql_verification import userInClass, getUsername, postInClass, checkPostOwner, checkCode


router = APIRouter(prefix='/classes/{code}/posts',tags=['Posts'])

@router.get("/", response_model=List[posts_schemas.PostOut])
def get_posts(code: int, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    posts = sqlQuery('SELECT * FROM posts WHERE code = %s;',(code,),fetchALL=True)
    return posts

@router.get("/{id}", response_model=posts_schemas.PostOut)
def get_post_by_id(code:int,id:int,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    if not postInClass(id,code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'post with {id} not found in class with code {code}')
    post = sqlQuery("SELECT * FROM posts WHERE post_id = %s;",(id,))
    return post

@router.post("/", response_model=posts_schemas.PostOut)
def make_post(data: posts_schemas.AddPost ,code: int, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    new_post = sqlQuery("INSERT INTO posts (code, user_id, title, content, user_name) VALUES (%s, %s, %s, %s, %s) RETURNING *;",(code,tokenData.id,data.title,data.content,getUsername(tokenData.id)))
    return new_post

@router.put("/{id}", response_model=posts_schemas.PostOut)
def update_post(data: posts_schemas.AddPost, code: int, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not postInClass(id,code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'post with {id} not found in class with code {code}')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User not in class')
    if not checkPostOwner(user_id=tokenData.id,post_id=id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User is not the owner of the post")
    updated_post = sqlQuery("UPDATE posts SET title = %s, content = %s WHERE post_id = %s AND user_id = %s RETURNING *;",(data.title,data.content,id,tokenData.id,))
    return updated_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(code: int, id: int ,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not postInClass(id,code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'post with {id} not found in class with code {code}')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User not in class')
    if not checkPostOwner(user_id=tokenData.id,post_id=id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User is not the owner of the post")
    deleted_post = sqlQuery("DELETE FROM posts WHERE post_id = %s, user_id = %s RETURNING *;",(id,tokenData.id,))
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No posts were deleted")

