from httpx import request
from passlib.context import CryptContext
import psycopg2, os, time, requests
from dotenv import load_dotenv
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException, status

load_dotenv()
db_user = os.getenv("DB_User")
db_pass = os.getenv("DB_User_PASS")
file_api = os.getenv("FILE_API")
email_api = os.getenv("EMAIL_API")



def sqlQuery(sql: str, params: tuple, fetchALL: bool = False):
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
    cur.execute(sql,params)
    try:
        if fetchALL:
            out = cur.fetchall()
        else:
            out = cur.fetchone()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='SQL query problem')
    conn.commit()
    conn.close()
    return out

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def getUserFolder():
    headers = {'X-API-Key':file_api}
    response = requests.get("https://hackclub.maksimmalbasa.in.rs/api/v1/folder/22136dfaa1c149fc4cdeda33a6bbc37b",headers=headers)
    return response.json()

def getSubmissionsFolder():
    headers = {'X-API-Key':file_api}
    response = requests.get("https://hackclub.maksimmalbasa.in.rs/api/v1/folder/1bb83e90e26a87f359f375091056aa93",headers=headers)
    return response.json()

def uploadSubmissionFile(file_name, byte_content, file_type):
    headers = {'X-API-Key':file_api}
    file = {'file': (file_name, byte_content, file_type)}
    response = requests.post("https://hackclub.maksimmalbasa.in.rs/api/v1/upload?folderId=1bb83e90e26a87f359f375091056aa93",files=file,headers=headers)
    response.raise_for_status()
    return response.json()

def getSubmissionFile(file_name):
    headers = {'X-API-Key':file_api}
    response = requests.get(f"https://hackclub.maksimmalbasa.in.rs/api/v1/file/1bb83e90e26a87f359f375091056aa93:{file_name}",stream=True,headers=headers)
    response.raise_for_status()
    content_type = response.headers.get('Content-Type', 'application/octet-stream')
    return (response, content_type)

def deleteSubmissionFile(file_name):
    headers = {'X-API-Key':file_api}
    response = requests.delete(f"https://hackclub.maksimmalbasa.in.rs/api/v1/delete/1bb83e90e26a87f359f375091056aa93/{file_name}",stream=True,headers=headers)
    response.raise_for_status()
    return response.json()

def askAI(prompt):
    headers = {"Content-Type":"application/json"}
    data = {'messages':[{"role": "user", "content": prompt}]}
    response = requests.post("https://ai.hackclub.com/chat/completions",headers=headers,json=data)
    response.raise_for_status()
    output = response.json()
    return output['choices'][0]['message']['content']

def createContact(email: str, name: str):
    headers = {"Authorization": f"Bearer {email_api}"}
    data = {"email":email, "firstName":name}
    response = requests.post("https://app.loops.so/api/v1/contacts/create",headers=headers,json=data)
    response.raise_for_status()
    output = response.json()
    return output

