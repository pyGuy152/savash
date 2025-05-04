from typing import List
from fastapi import APIRouter, status, HTTPException
import psycopg2, os, time
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from .. import schemas, utils

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


router = APIRouter(prefix='/users',tags=['Users'])

def check_user(username: str, email: str):
    cur.execute("SELECT * FROM users WHERE username = %s OR email = %s;",(username,email,))
    user = cur.fetchone()
    if not user:
        return False
    else:
        return True

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def make_user(user_cred: schemas.UserCreate):
    if check_user(user_cred.username,user_cred.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email aldready taken")
    user_cred.password = utils.get_password_hash(user_cred.password)
    cur.execute("INSERT INTO users (name, username, email, password, role) VALUES (%s,%s,%s,%s,%s) RETURNING *;",(user_cred.name,user_cred.username,user_cred.email,user_cred.password,user_cred.role,))
    new_user = cur.fetchone()
    conn.commit()
    return new_user

@router.get('/', response_model=List[schemas.UserOut])
def get_all_users():
    cur.execute("SELECT * FROM users;")
    all_users = cur.fetchall()
    return all_users

@router.get('/{username}', response_model=schemas.UserOut)
def get_user(username: str):
    cur.execute("SELECT * FROM users WHERE username = %s;",(username,))
    user = cur.fetchone()
    return user

@router.put('/{username}', response_model=schemas.UserOut)
def update_user(user_cred: schemas.UserCreate, username :str):
    if check_user(user_cred.username,user_cred.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email aldready taken")
    user_cred.password = utils.get_password_hash(user_cred.password)
    cur.execute("UPDATE users SET name = %s, username = %s, email = %s, password = %s, role = %s WHERE username = %s RETURNING *;",(user_cred.name,user_cred.username,user_cred.email,user_cred.password,user_cred.role,username,))
    new_user = cur.fetchone()
    conn.commit()
    return new_user