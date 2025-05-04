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


router = APIRouter(prefix='/class',tags=['Classes'])

@router.post("/", response_model=schemas.ClassOut, status_code=status.HTTP_201_CREATED)
def make_class(class_data: schemas.ClassMake):
    code = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
    cur.execute("INSERT INTO class (code, name) VALUES (%s,%s) RETURNING *;",(code,class_data.name,))
    conn.commit()
    new_class = cur.fetchone()
    return new_class

@router.get("/", response_model=List[schemas.ClassOut])
def get_class():
    cur.execute("SELECT * FROM class;")
    classes = cur.fetchall()
    return classes