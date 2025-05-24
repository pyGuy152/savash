from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from .. import oauth2
from ..schemas import assignments_schemas
from ..utils import sqlQuery, uploadSubmissionFile, getSubmissionFile
import random, os

router = APIRouter(prefix='/classes/{code}/assignments/{id}/submit',tags=['Submit'])

def userInClass(id,code):
    x = sqlQuery("SELECT * FROM user_class WHERE user_id = %s AND code = %s;",(id,code,))
    if not x or x == None:
        return False
    return True

@router.post("/written")
async def upload_written_submissions(code: int, id: int ,file : UploadFile = File(...)):
    contents = await file.read()
    response = uploadSubmissionFile(file.filename, contents, file.content_type)
    out = sqlQuery("INSERT INTO submissions (user_id, assignment_id, submission_path, grade) VALUES (%s, %s, %s, %s) RETURNING *;",(21,id,response["files"][0]["name"],None,))
    return out

@router.get("/written")
def get_written_submissions(code: int, id: int):
    file_name = sqlQuery("SELECT * FROM submissions WHERE assignment_id = %s AND user_id = %s;",(id,21,))
    if file_name:
        if getSubmissionFile(file_name=file_name["submission_path"],file_path=f'app/temp_files/{file_name["submission_path"]}'): # type: ignore
            return FileResponse(f'app/temp_files/{file_name["submission_path"]}') # type: ignore