from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from .. import oauth2
from ..schemas import assignments_schemas
from ..utils import sqlQuery, uploadSubmissionFile, getSubmissionFile, deleteSubmissionFile
from ..sql_verification import assignmentInClass, userInClass, verifyTeacher
import random, os

router = APIRouter(prefix='/classes/{code}/assignments/{id}/submit',tags=['Submit'])

@router.post("/written")
async def upload_written_submissions(code: int, id: int ,file : UploadFile = File(...), tokenData = Depends(oauth2.get_current_user)):
    if not assignmentInClass(id,code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'assignment with id {id} not in class with code {code}')
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in class")
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a teacher")
    contents = await file.read()
    x = sqlQuery("SELECT * FROM submissions WHERE assignment_id = %s;",(id,))
    response = uploadSubmissionFile(file.filename, contents, file.content_type)
    if x:
        del_response = deleteSubmissionFile(x["submission_path"]) # type: ignore
        if not del_response:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        out = sqlQuery("UPDATE submissions SET submission_path = %s WHERE assignment_id = %s RETURNING *;",(response["files"][0]["name"],id,))
    else:
        out = sqlQuery("INSERT INTO submissions (user_id, assignment_id, submission_path, grade) VALUES (%s, %s, %s, %s) RETURNING *;",(tokenData.id,id,response["files"][0]["name"],None,))
    return out

@router.get("/written")
def get_written_submissions(code: int, id: int, tokenData = Depends(oauth2.get_current_user)):
    if not userInClass(tokenData.id,code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in class")
    if not assignmentInClass(id,code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'assignment with id {id} not in class with code {code}')
    file_name = sqlQuery("SELECT * FROM submissions WHERE assignment_id = %s AND user_id = %s;",(id,tokenData.id,))
    if file_name:
        x = getSubmissionFile(file_name=file_name["submission_path"]) # type: ignore
        if x:
            return StreamingResponse(x[0].iter_content(chunk_size=8192),media_type=x[1])
        
