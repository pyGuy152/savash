from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File
from .. import utils, oauth2, run_code
import os

router = APIRouter(prefix='/run',tags=['Run Code'])

@router.post("/")
async def run_python_code(file : UploadFile = File(...), tokenData = Depends(oauth2.get_current_user)):
    if not 'python' in str(file.content_type):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please send a python file")
    contents = await file.read()
    with open(f"app/sandbox/{file.filename}",'wb') as f:
        f.write(contents)
    out = run_code.run_code(str(file.filename))
    os.remove(f"app/sandbox/{file.filename}")
    return out

