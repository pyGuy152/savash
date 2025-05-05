from pickletools import int4
from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
import psycopg2, os, time
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


router = APIRouter(prefix='/users',tags=['Users'])

def check_user(email: str):
    cur.execute("SELECT * FROM users WHERE email = %s;",(email,))
    user = cur.fetchone()
    if not user:
        return False
    else:
        return True

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def make_user(user_cred: schemas.UserCreate):
    if check_user(user_cred.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email aldready taken")
    user_cred.password = utils.get_password_hash(user_cred.password)
    cur.execute("INSERT INTO users (name, username, email, password, role) VALUES (%s,%s,%s,%s,%s) RETURNING *;",(user_cred.name,user_cred.username,user_cred.email,user_cred.password,user_cred.role,))
    new_user = cur.fetchone()
    conn.commit()
    return new_user

@router.get('/', response_model=schemas.UserOut)
def get_user(tokenData = Depends(oauth2.get_current_user)):
    cur.execute("SELECT * FROM users WHERE user_id = %s;",(tokenData.id,))
    user = cur.fetchone()
    if not user['join_req']: # type: ignore
        user['join_req'] = [] # type: ignore
    return user

@router.put('/', response_model=schemas.UserOut)
def update_user(user_cred: schemas.UserCreate, tokenData = Depends(oauth2.get_current_user)):
    if check_user(user_cred.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email aldready taken")
    user_cred.password = utils.get_password_hash(user_cred.password)
    cur.execute("UPDATE users SET name = %s, username = %s, email = %s, password = %s, role = %s WHERE user_id = %s RETURNING *;",(user_cred.name,user_cred.username,user_cred.email,user_cred.password,user_cred.role,tokenData.id,))
    new_user = cur.fetchone()
    conn.commit()
    return new_user

@router.delete('/',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(tokenData = Depends(oauth2.get_current_user)):
    cur.execute("DELETE FROM users WHERE user_id = %s RETURNING *;", (tokenData.id,))
    del_user = cur.fetchone()
    conn.commit()
    if not del_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No user deleted")