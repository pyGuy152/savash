from fastapi import APIRouter, status, HTTPException
import psycopg2, os, time
from psycopg2 import Error
from dotenv import load_dotenv
from .. import schemas

load_dotenv()
db_user = os.getenv("DB_User")
db_pass = os.getenv("DB_User_PASS")

# connect and create a cursor for the db
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


router = APIRouter(prefix='/users',tags=['Users'])

def check_user(username: str, email: str):
    cur.execute("SELECT * FROM users WHERE username = %s OR email = %s;",(username,email,))
    user = cur.fetchone()
    if not user:
        return False
    else:
        return True

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def get_users(user_cred: schemas.UserCreate):
    if check_user(user_cred.username,user_cred.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email aldready taken")
    cur.execute("INSERT INTO users (name, username, email, password, role) VALUES (%s,%s,%s,%s,%s) RETURNING *;",(user_cred.name,user_cred.username,user_cred.email,user_cred.password,user_cred.role,))
    new_user = cur.fetchone()
    conn.commit()
    return {"Message":"User created"}