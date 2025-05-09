from passlib.context import CryptContext
import psycopg2, os, time
from dotenv import load_dotenv
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException, status

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

def sqlQuery(sql: str, params: tuple, fetchALL: bool = False):
    cur.execute(sql,params)
    try:
        if fetchALL:
            out = cur.fetchall()
        else:
            out = cur.fetchone()
    except:
        return 
    conn.commit()
    return out

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

