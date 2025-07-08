from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File
from .. import oauth2
from ..schemas import assignments_schemas
from ..utils import sqlQuery, uploadSubmissionFile
from ..sql_verification import checkCode, validateMcq, validateCoding, validateTfq, verifyTeacher, userInClass, assignmentInClass
import random

router = APIRouter(prefix='/classes/{code}/assignments',tags=['Assignments'])

def getNewAssignmentId():
    id = str(random.randint(0,1000000))
    x = sqlQuery("SELECT title FROM written WHERE assignment_id = %s;",(id,),fetchALL=True)
    y = sqlQuery("SELECT title FROM mcq WHERE assignment_id = %s;",(id,),fetchALL=True)
    z = sqlQuery("SELECT title FROM frq WHERE assignment_id = %s;",(id,),fetchALL=True)
    v = sqlQuery("SELECT title FROM tfq WHERE assignment_id = %s;",(id,),fetchALL=True)
    while (x or y or z or v):
        id = str(random.randint(0,1000000))
        x = sqlQuery("SELECT title FROM written WHERE assignment_id = %s;",(id,),fetchALL=True)
        y = sqlQuery("SELECT title FROM mcq WHERE assignment_id = %s;",(id,),fetchALL=True)
        z = sqlQuery("SELECT title FROM frq WHERE assignment_id = %s;",(id,),fetchALL=True)
        v = sqlQuery("SELECT title FROM tfq WHERE assignment_id = %s;",(id,),fetchALL=True)
    return id

@router.post("/written", response_model=assignments_schemas.AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_written_assignment(code:int,data:assignments_schemas.WrittenAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant create assigments')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    new_assignment = sqlQuery('INSERT INTO written (assignment_id, title, description, due_date, points, code) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;',(getNewAssignmentId(),data.title,data.description,data.due_date,data.points,code,))
    if not new_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No new assignments were created")
    return new_assignment

@router.post("/mcq", response_model=assignments_schemas.AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_mcq_assignment(code:int,data:assignments_schemas.MCQAssignment,tokenData = Depends(oauth2.get_current_user)):
    validateMcq(data)
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant create assigments')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    new_assignment = sqlQuery('INSERT INTO mcq (assignment_id, title, description, due_date, points, questions, choices, correct_answer, code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;',(getNewAssignmentId(),data.title,data.description,data.due_date,data.points,data.questions,data.choices,data.correct_answer,code,))
    if not new_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No new assignments were created")
    return new_assignment

@router.post("/frq", response_model=assignments_schemas.AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_frq_assignment(code:int,data:assignments_schemas.FRQAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant create assigments')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    new_assignment = sqlQuery('INSERT INTO frq (assignment_id, title, description, due_date, points, questions, code) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;',(getNewAssignmentId(),data.title,data.description,data.due_date,data.points,data.questions,code,))
    if not new_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No new assignments were created")
    return new_assignment

@router.post("/tfq", response_model=assignments_schemas.AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_tfq_assignment(code:int,data:assignments_schemas.TFQAssignment,tokenData = Depends(oauth2.get_current_user)):
    validateTfq(data)
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant create assigments')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    new_assignment = sqlQuery('INSERT INTO tfq (assignment_id, title, description, due_date, points, questions, correct_answer, code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;',(getNewAssignmentId(),data.title,data.description,data.due_date,data.points,data.questions, data.correct_answer,code,))
    if not new_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No new assignments were created")
    return new_assignment

@router.post("/coding", response_model=assignments_schemas.AssignmentOut, status_code=status.HTTP_201_CREATED)
async def create_coding_assignment(code:int,data:assignments_schemas.CodingAssignment,code_file : UploadFile = File(...),tokenData = Depends(oauth2.get_current_user)):
    validateCoding(data)
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant create assigments')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    contents = await code_file.read()
    response = uploadSubmissionFile(code_file.filename, contents, code_file.content_type)
    new_assignment = sqlQuery('INSERT INTO coding (assignment_id, title, description, due_date, points, input, output, code, code_file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;',(getNewAssignmentId(),data.title,data.description,data.due_date,data.points,data.input, data.output,code,response["files"][0]["name"],))
    if not new_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No new assignments were created")
    return new_assignment

@router.get("/", response_model=List[assignments_schemas.AssignmentOut])
def get_assignments(code: int, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    written = sqlQuery("SELECT * FROM written WHERE code = %s;",(code,),fetchALL=True)
    mcq = sqlQuery("SELECT * FROM mcq WHERE code = %s;",(code,),fetchALL=True)
    frq = sqlQuery("SELECT * FROM frq WHERE code = %s;",(code,),fetchALL=True)
    tfq = sqlQuery("SELECT * FROM tfq WHERE code = %s;",(code,),fetchALL=True)
    coding = sqlQuery("SELECT * FROM coding WHERE code = %s;",(code,),fetchALL=True)
    if not written:
        written = []
    elif isinstance(written,tuple):
        written = [written]
    if not mcq:
        mcq = []
    elif isinstance(mcq,tuple):
        mcq = [mcq]
    if not frq:
        frq = []
    elif isinstance(frq,tuple):
        frq = [frq]
    if not tfq:
        tfq = []
    elif isinstance(tfq,tuple):
        tfq = [tfq]
    if not coding:
        coding = []
    elif isinstance(coding,tuple):
        coding = [coding]
    return written + mcq + frq + tfq + coding

@router.get("/{id}")
def get_assignment_by_id(code: int, id: int, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    if not assignmentInClass(id,code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Assignment with id {id} not found in class")
    written = sqlQuery("SELECT * FROM written WHERE code = %s AND assignment_id = %s;",(code,id,))
    mcq = sqlQuery("SELECT * FROM mcq WHERE code = %s AND assignment_id = %s;",(code,id,))
    frq = sqlQuery("SELECT * FROM frq WHERE code = %s AND assignment_id = %s;",(code,id,))
    tfq = sqlQuery("SELECT * FROM tfq WHERE code = %s AND assignment_id = %s;",(code,id,))
    coding = sqlQuery("SELECT * FROM coding WHERE code = %s AND assignment_id = %s;",(code,id,))
    if written:
        return written
    elif mcq:
        return mcq
    elif frq:
        return frq
    elif tfq:
        return tfq
    elif coding:
        return coding
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")


@router.put("/", response_model=assignments_schemas.AssignmentOut)
def update_assignment(code:int, data:assignments_schemas.UpdateAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant Update assigments')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    if data.questions and data.choices and data.correct_answer:
        validateMcq(data)
        try_update_mcq_assignment = sqlQuery("UPDATE mcq SET title = %s, description = %s, questions = %s , choices = %s , correct_answer = %s ,due_date = %s, points = %s WHERE assignment_id = %s RETURNING *;",(data.title,data.description,data.questions,data.choices,data.correct_answer,data.due_date,data.points,data.assignment_id,))
    elif data.questions and data.correct_answer:
        validateTfq(data)
        try_update_tfq_assignment = sqlQuery("UPDATE tfq SET title = %s, description = %s, questions = %s ,correct_answer = %s ,due_date = %s, points = %s WHERE assignment_id = %s RETURNING *;",(data.title,data.description,data.questions,data.correct_answer,data.due_date,data.points,data.assignment_id,))
    elif data.questions:
        try_update_frq_assignment = sqlQuery("UPDATE frq SET title = %s, description = %s, questions = %s ,due_date = %s, points = %s WHERE assignment_id = %s RETURNING *;",(data.title,data.description,data.questions,data.due_date,data.points,data.assignment_id,))
    elif data.input and data.output:
        try_update_coding_assignment = sqlQuery("UPDATE coding SET title = %s, description = %s, input = %s, output = %s, due_date = %s, points = %s WHERE assignment_id = %s RETURNING *;",(data.title,data.description,data.input,data.output,data.due_date,data.points,data.assignment_id,))
    else:
        try_update_written_assignment = sqlQuery("UPDATE written SET title = %s, description = %s, due_date = %s, points = %s WHERE assignment_id = %s RETURNING *;",(data.title,data.description,data.due_date,data.points,data.assignment_id,))

    if try_update_mcq_assignment:
        return try_update_mcq_assignment
    elif try_update_tfq_assignment:
        return try_update_tfq_assignment
    elif try_update_frq_assignment:
        return try_update_frq_assignment
    elif try_update_written_assignment:
        return try_update_written_assignment
    elif try_update_coding_assignment:
        return try_update_coding_assignment
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='No assignments were updated')

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(code:int,data:assignments_schemas.DeleteAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant Update assigments')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    del_written_assignment = sqlQuery("DELETE FROM written WHERE assignment_id = %s AND code = %s RETURNING *;",(data.assignment_id,code,))
    del_frq_assignment = sqlQuery("DELETE FROM frq WHERE assignment_id = %s AND code = %s RETURNING *;",(data.assignment_id,code,))
    del_mcq_assignment = sqlQuery("DELETE FROM mcq WHERE assignment_id = %s AND code = %s RETURNING *;",(data.assignment_id,code,))
    del_tfq_assignment = sqlQuery("DELETE FROM tfq WHERE assignment_id = %s AND code = %s RETURNING *;",(data.assignment_id,code,))
    del_coding_assignment = sqlQuery("DELETE FROM coding WHERE assignment_id = %s AND code = %s RETURNING *;",(data.assignment_id,code,))
    if not del_written_assignment and not del_frq_assignment and not del_mcq_assignment and not del_tfq_assignment and not del_coding_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No assignments were deleted")

