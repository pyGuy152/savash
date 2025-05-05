from pickletools import int4
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
        print("connected to db")
        break
    except Error as e:
        if conn:
            conn.close()
        print(f"Error connecting to DB: {e}")
        time.sleep(5)


router = APIRouter(prefix='/classes',tags=['Classes'])

def checkCode(code):
    cur.execute("SELECT * FROM class WHERE code = %s;",(str(code),))
    if cur.fetchone():
        return True
    else:
        return False

def checkEmail(email):
    cur.execute("SELECT * FROM users WHERE email = %s;",(str(email),))
    if cur.fetchone():
        return True
    else:
        return False

def getUserId(email):
    cur.execute("SELECT * FROM users WHERE email = %s;",(str(email),))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="not a valid email")
    return user['user_id'] # type: ignore

def verifyOwnerOf(id):
    cur.execute("SELECT * FROM users WHERE user_id = %s AND role = 'teacher'",(id,))
    relation = cur.fetchone()
    if relation:
        return True
    else:
        return False

@router.post("/", response_model=schemas.ClassOut, status_code=status.HTTP_201_CREATED)
def make_class(class_data: schemas.ClassMake, tokenData = Depends(oauth2.get_current_user)):
    code = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
    while checkCode(code):
        code = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
    cur.execute("INSERT INTO class (code, name) VALUES (%s,%s) RETURNING *;",(code,class_data.name,))
    conn.commit()
    new_class = cur.fetchone()
    cur.execute("INSERT INTO user_class (user_id, code) VALUES (%s, %s);",(tokenData.id,code))
    conn.commit()
    return new_class

@router.get("/", response_model=List[schemas.ClassOut])
def get_class(tokenData = Depends(oauth2.get_current_user)):
    cur.execute("SELECT c.code, c.name, c.created_at FROM class c JOIN user_class uc ON c.code = uc.code JOIN users u ON uc.user_id = u.user_id WHERE u.user_id = %s AND u.role = 'teacher';",(tokenData.id,))
    classes = cur.fetchall()
    return classes

@router.post("/add")
def add_student_to_class(inviteData:schemas.ClassUsers, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(inviteData.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not checkEmail(inviteData.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid email')
    if not verifyOwnerOf(tokenData.id):
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to add users to this class")
    cur.execute("UPDATE users SET join_req = array_append(join_req, %s) WHERE email = %s RETURNING *;",(inviteData.code,inviteData.email))
    conn.commit()
    if cur.fetchone():
        return {'message':'invite sent!!!'}
    else:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='No invites sent')

@router.post("/remove")
def remove_student_from_class(removeData:schemas.ClassUsers, tokenData = Depends(oauth2.get_current_user)):
    if not checkCode(removeData.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid code')
    if not checkEmail(removeData.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='not a valid email')
    if not verifyOwnerOf(tokenData.id):
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to remove users from this class")
    cur.execute("DELETE FROM user_class WHERE code = %s AND user_id = %s RETURNING *;",(removeData.code,getUserId(removeData.email),))
    removed = cur.fetchone()
    conn.commit()
    cur.execute("UPDATE users SET join_req = array_remove(join_req, %s) WHERE email = %s RETURNING *;",(removeData.code,removeData.email))
    removed_1 = cur.fetchone()
    conn.commit()
    if not removed_1 and not removed:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Did not remove from class')
    else:
        return {"message":"Removed from class"}
