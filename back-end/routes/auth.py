from fastapi import APIRouter, HTTPException, status
import os, time, psycopg2
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


router = APIRouter(tags=['Auth'])

@router.post("/login")
def login(user_cred: schemas.LoginInput):
    cur.execute("SELECT * FROM users WHERE email = %s;",(user_cred.email,))
    hashed_pass = cur.fetchone()
    try:
        if utils.verify_password(user_cred.password,hashed_pass['password']): # type: ignore
            access_token = oauth2.create_access_token(data = {"user_id": hashed_pass['user_id']}) # type: ignore
            return {'access_token':access_token, 'token_type':"bearer"}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")