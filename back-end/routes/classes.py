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

def verifyTeacher(id):
    cur.execute("SELECT * FROM users WHERE user_id = %s AND role = 'teacher'",(id,))
    relation = cur.fetchone()
    if relation:
        return True
    else:
        return False

def verifyOwner(code,id):
    cur.execute("SELECT * FROM class WHERE owner = %s AND code = %s;",(id,code,))
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
    if verifyTeacher(tokenData.id):
        cur.execute("INSERT INTO class (code, name, owner) VALUES (%s,%s,%s) RETURNING *;",(code,class_data.name,tokenData.id,))
        conn.commit()
        new_class = cur.fetchone()
        cur.execute("INSERT INTO user_class (user_id, code) VALUES (%s, %s);",(tokenData.id,code))
        conn.commit()
        return new_class
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to create a class")

@router.get("/", response_model=List[schemas.ClassOut])
def get_class(tokenData = Depends(oauth2.get_current_user)):
    cur.execute("SELECT c.code, c.name, c.created_at FROM class c JOIN user_class uc ON c.code = uc.code JOIN users u ON uc.user_id = u.user_id WHERE u.user_id = %s;",(tokenData.id,))
    classes = cur.fetchall()
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
    if not verifyOwner(removeData.code,tokenData.id):
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

@router.put('/')
def update_class(data:schemas.UpdateClass,tokenData = Depends(oauth2.get_current_user)):
    if verifyOwner(data.code,tokenData.id):
        cur.execute("UPDATE class SET name = %s WHERE code = %s RETURNING *;",(data.name,data.code,))
        updated_class = cur.fetchone()
        conn.commit()
        if not updated_class:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Could not update class')
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to update this class")

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_class(data:schemas.DelClass,tokenData = Depends(oauth2.get_current_user)):
    if verifyOwner(data.code,tokenData.id):
        cur.execute("DELETE FROM class WHERE code = %s RETURNING *;",(data.code,))
        deleted_class = cur.fetchone()
        conn.commit()
        if not deleted_class:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,detail='Could not delete class')
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail="You dont have permission to delete this class")

@router.post('/join')
def join_a_class(data: schemas.JoinClass, tokenData = Depends(oauth2.get_current_user)):
    if not verifyTeacher(tokenData.id):
        cur.execute("INSERT INTO user_class (user_id,code) VALUES (%s, %s) RETURNING *;",(tokenData.id,data.code,))
        relation = cur.fetchone()
        conn.commit()
        return relation
    else:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="nuh uh")

