from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from .. import oauth2
from ..schemas import assignments_schemas
from ..utils import sqlQuery

router = APIRouter(prefix='/classes/assignments',tags=['Assignments'])

def verifyTeacher(id):
    x = sqlQuery("SELECT * FROM users WHERE user_id = %s AND role = 'teacher'",(id,))
    if not x or x == None:
        return False
    return True

def userInClass(id,code):
    x = sqlQuery("SELECT * FROM user_class WHERE user_id = %s AND code = %s;",(id,code,))
    if not x or x == None:
        return False
    return True

def checkCode(code):
    x = sqlQuery("SELECT * FROM class WHERE code = %s;",(str(code),))
    if not x or x == None:
        return False
    return True

@router.post("/", response_model=assignments_schemas.AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_assignment(data:assignments_schemas.MakeAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(data.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant create assigments')
    if not userInClass(tokenData.id,data.code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    new_assignment = sqlQuery("INSERT INTO assignments (code, title, description, due_date) VALUES (%s,%s,%s,%s) RETURNING *;",(data.code,data.title,data.description,data.due_date,))
    if not new_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No new assignments were created")
    return new_assignment

@router.get("/{code}", response_model=List[assignments_schemas.AssignmentOut])
def get_assignments(code: int, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    assignments = sqlQuery("SELECT * FROM assignments WHERE code = %s;",(code,),fetchALL=True)
    return assignments

@router.put("/", response_model=assignments_schemas.AssignmentOut)
def update_assignment(data:assignments_schemas.UpdateAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(data.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant Update assigments')
    if not userInClass(tokenData.id,data.code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    new_assignment = sqlQuery("UPDATE assignments SET code = %s, title = %s, description = %s, due_date = %s WHERE assignment_id = %s RETURNING *;",(data.code,data.title,data.description,data.due_date,data.assignment_id,))
    if not new_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No new assignments were created")
    return new_assignment

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(data:assignments_schemas.DeleteAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(data.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant Update assigments')
    if not userInClass(tokenData.id,data.code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    del_assignment = sqlQuery("DELETE FROM assignments WHERE assignment_id = %s AND code = %s RETURNING *;",(data.assignment_id,data.code,))
    if not del_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No assignments were deleted")

