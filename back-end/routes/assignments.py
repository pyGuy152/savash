from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
import psycopg2, os, time, random
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from .. import schemas, utils, oauth2

load_dotenv()
db_user = os.getenv("DB_User")
db_pass = os.getenv("DB_User_PASS")

# connect and create a cursor for the db
while True:
    try:
        conn = psycopg2.connect(database='savash',user=db_user,password=db_pass,host='localhost',port='5432',cursor_factory=RealDictCursor)
        cur = conn.cursor()
        break
    except Error as e:
        if conn:
            conn.close()
        print(f"Error connecting to DB: {e}")
        time.sleep(5)


router = APIRouter(prefix='/classes/assignments',tags=['Assignments'])

def verifyTeacher(id):
    cur.execute("SELECT * FROM users WHERE user_id = %s AND role = 'teacher'",(id,))
    relation = cur.fetchone()
    if relation:
        return True
    else:
        return False

def userInClass(id,code):
    cur.execute("SELECT * FROM user_class WHERE user_id = %s AND code = %s;",(id,code,))
    relation = cur.fetchone()
    if relation:
        return True
    else:
        return False

def checkCode(code):
    cur.execute("SELECT * FROM class WHERE code = %s;",(str(code),))
    if cur.fetchone():
        return True
    else:
        return False

@router.get("/", response_model=List[schemas.AssignmentOut])
def get_assignments(data:schemas.ClassBase,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(data.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not userInClass(tokenData.id,data.code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    cur.execute("SELECT * FROM assignments WHERE code = %s;",(data.code,))
    assignments = cur.fetchall()
    return assignments

@router.post("/", response_model=schemas.AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_assignment(data:schemas.MakeAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(data.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant create assigments')
    if not userInClass(tokenData.id,data.code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    cur.execute("INSERT INTO assignments (code, title, description, due_date) VALUES (%s,%s,%s,%s) RETURNING *;",(data.code,data.title,data.description,data.due_date,))
    new_assignment = cur.fetchone()
    conn.commit()
    if not new_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No new assignments were created")
    return new_assignment

@router.put("/", response_model=schemas.AssignmentOut)
def update_assignment(data:schemas.UpdateAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(data.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant Update assigments')
    if not userInClass(tokenData.id,data.code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    cur.execute("UPDATE assignments SET code = %s, title = %s, description = %s, due_date = %s WHERE assignment_id = %s RETURNING *;",(data.code,data.title,data.description,data.due_date,data.assignment_id,))
    new_assignment = cur.fetchone()
    conn.commit()
    if not new_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No new assignments were created")
    return new_assignment

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(data:schemas.DeleteAssignment,tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(data.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant Update assigments')
    if not userInClass(tokenData.id,data.code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    cur.execute("DELETE FROM assignments WHERE assignment_id = %s AND code = %s RETURNING *;",(data.assignment_id,data.code,))
    del_assignment = cur.fetchone()
    conn.commit()
    if not del_assignment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error, No assignments were deleted")