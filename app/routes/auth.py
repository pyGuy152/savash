from fastapi import APIRouter
import os, time, psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
from .. import schemas

load_dotenv()
db_user = os.getenv("DB_User")
db_pass = os.getenv("DB_User_PASS")

# connect and create a cursor for the db
conn = None
cur = None
while True:
    try:
        conn = psycopg2.connect(database='savash',user=db_user,password=db_pass,host='localhost',port='5432')
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
    return {'data':user_cred}