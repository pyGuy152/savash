from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File
from .. import utils, oauth2, run_code
from ..schemas import run_schemas
import os

router = APIRouter(prefix='/run',tags=['Run Code'])

@router.post("/python")
async def run_python_code(file : UploadFile = File(...), tokenData = Depends(oauth2.get_current_user)):
    if not 'python' in str(file.content_type):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please send a python file")
    contents = await file.read()
    with open(f"app/sandbox/{file.filename}",'wb') as f:
        f.write(contents)
    out = run_code.run_code(str(file.filename))
    os.remove(f"app/sandbox/{file.filename}")
    return out

@router.post("/python/testcases")
async def run_python_code_with_testcases(data : run_schemas.Testcases, file : UploadFile = File(...)):
    if not 'python' in str(file.content_type):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please send a python file")
    if len(data.inputs) == len(data.outputs):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Testcase inputs and outputs length dont match")
    
    contents = await file.read()
    with open(f"app/sandbox/{file.filename}",'wb') as f:
        f.write(contents)
    
    out = []    
    for i in range(len(data.inputs)):
        result = run_code.run_code(str(file.filename),data.inputs[i])
        check = False
        if result == data.outputs[i]:
            check = True
        out.append({'expected':data.outputs[i],'actual':result,'match':check})
    
    os.remove(f"app/sandbox/{file.filename}")

    return out

