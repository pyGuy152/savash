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

@router.get("/", response_model=List[schemas.AssignmentOut])
def get_assignments(data:schemas.ClassBase,tokenData = Depends(oauth2.get_current_user)):
    if not userInClass(tokenData.id,data.code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not in this class')
    cur.execute("SELECT * FORM assignments WHERE code = %s;",(data.code,))
    assignments = cur.fetchall()
    return assignments

@router.post("/", response_model=schemas.AssignmentOut)
def create_assignment(data:schemas.ClassBase,tokenData = Depends(oauth2.get_current_user)):
    if not verifyTeacher(tokenData.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Students cant create assigments')
    