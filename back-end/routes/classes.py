from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
import random
from .. import schemas, oauth2
from ..utils import sqlQuery


router = APIRouter(prefix='/classes',tags=['Classes'])

def checkCode(code):
    x = sqlQuery("SELECT * FROM class WHERE code = %s;",(str(code),))
    if not x or x == None:
        return False
    return True
    

def checkEmail(email):
    x = sqlQuery("SELECT * FROM users WHERE email = %s;",(str(email),))
    if not x or x == None:
        return False
    return True

def getUserId(email):
    user = sqlQuery("SELECT * FROM users WHERE email = %s;",(str(email),))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="not a valid email")
    return user['user_id'] # type: ignore

def verifyTeacher(id):
    x = sqlQuery("SELECT * FROM users WHERE user_id = %s AND role = 'teacher'",(id,))
    if not x or x == None:
        return False
    return True

def verifyOwner(code,id):
    x = sqlQuery("SELECT * FROM class WHERE owner = %s AND code = %s;",(id,code,))
    if not x or x == None:
        return False
    return True

def checkIfInvitedT(code,id):
    x = sqlQuery("SELECT * FROM users WHERE %s = ANY(join_req) AND user_id = %s AND role = 'teacher';", (code,id,))
    if not x or x == None:
        return False
    return True

def userInClass(id,code):
    x = sqlQuery("SELECT * FROM user_class WHERE user_id = %s AND code = %s;",(id,code,))
    if not x or x == None:
        return False
    return True

@router.post("/", response_model=schemas.ClassOut, status_code=status.HTTP_201_CREATED)
def make_class(class_data: schemas.ClassMake, tokenData = Depends(oauth2.get_current_user)):
    code = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
    while checkCode(code):
        code = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
    if verifyTeacher(tokenData.id):
        new_class = sqlQuery("INSERT INTO class (code, name, owner) VALUES (%s,%s,%s) RETURNING *;",(code,class_data.name,tokenData.id,))
        sqlQuery("INSERT INTO user_class (user_id, code) VALUES (%s, %s);",(tokenData.id,code))
        return new_class
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to create a class")

@router.get("/", response_model=List[schemas.ClassOut])
def get_class(tokenData = Depends(oauth2.get_current_user)):
    classes = sqlQuery("SELECT c.code, c.name, c.created_at FROM class c JOIN user_class uc ON c.code = uc.code JOIN users u ON uc.user_id = u.user_id WHERE u.user_id = %s;",(tokenData.id,),fetchALL=True)
    return classes

@router.post("/add")
def add_student_to_class(inviteData:schemas.ClassUsers, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(inviteData.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not checkEmail(inviteData.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid email')
    if not verifyOwner(inviteData.code,tokenData.id):
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to add users to this class")
    if int(getUserId(inviteData.email)) == int(tokenData.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User tried to add themself")
    x = sqlQuery("UPDATE users SET join_req = array_append(join_req, %s) WHERE email = %s RETURNING *;",(inviteData.code,inviteData.email))
    if x:
        return {'message':'invite sent!!!'}
    else:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='No invites sent')

@router.post("/remove")
def remove_student_from_class(removeData:schemas.ClassUsers, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(removeData.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not checkEmail(removeData.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid email')
    if not verifyOwner(removeData.code,tokenData.id):
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to remove users from this class")
    removed = sqlQuery("DELETE FROM user_class WHERE code = %s AND user_id = %s RETURNING *;",(removeData.code,getUserId(removeData.email),))
    removed_1 = sqlQuery("UPDATE users SET join_req = array_remove(join_req, %s) WHERE email = %s RETURNING *;",(removeData.code,removeData.email))
    if not removed_1 and not removed:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Did not remove from class')
    else:
        return {"message":"Removed from class"}

@router.put('/',response_model=List[schemas.ClassOut])
def update_class(data:schemas.UpdateClass,tokenData = Depends(oauth2.get_current_user)):
    if verifyOwner(data.code,tokenData.id):
        updated_class = sqlQuery("UPDATE class SET name = %s WHERE code = %s RETURNING *;",(data.name,data.code,))
        if not updated_class:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Could not update class')
        return updated_class
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to update this class")

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_class(data:schemas.DelClass,tokenData = Depends(oauth2.get_current_user)):
    if verifyOwner(data.code,tokenData.id):
        deleted_class = sqlQuery("DELETE FROM class WHERE code = %s RETURNING *;",(data.code,))
        if not deleted_class:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Could not delete class')
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to delete this class")

@router.post('/join')
def join_a_class(data: schemas.JoinClass, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(data.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id) or checkIfInvitedT(data.code,tokenData.id):
        relation = sqlQuery("INSERT INTO user_class (user_id,code) VALUES (%s, %s) RETURNING *;",(tokenData.id,data.code,))
        removed_invite = sqlQuery("UPDATE users SET join_req = array_remove(join_req, %s) WHERE user_id = %s RETURNING *;",(data.code,tokenData.id))
        return relation
    else:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="nuh uh")

@router.get("/{code}")
def get_one_class(code: int, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This code doesnt exist")
    if userInClass(tokenData.id,code):
        class_out = sqlQuery("SELECT c.code, c.name, c.created_at FROM class c JOIN user_class uc ON c.code = uc.code JOIN users u ON uc.user_id = u.user_id WHERE u.user_id = %s AND u.role = 'teacher' AND uc.code = %s;",(tokenData.id,code,))
        return class_out
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You cannot access this info')

