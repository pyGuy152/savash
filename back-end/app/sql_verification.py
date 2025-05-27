from fastapi import HTTPException, status
from .utils import sqlQuery

def checkEmail(email):
    x = sqlQuery("SELECT * FROM users WHERE email = %s;",(str(email),))
    if not x or x == None:
        return False
    return True

def getUserId(email):
    user = sqlQuery("SELECT user_id FROM users WHERE email = %s;",(str(email),))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="not a valid email")
    return user['user_id'] # type: ignore

def verifyOwner(code,id):
    x = sqlQuery("SELECT * FROM class WHERE owner = %s AND code = %s;",(id,code,))
    if not x or x == None:
        return False
    return True

def checkIfInvited(code,id):
    x = sqlQuery("SELECT * FROM users WHERE %s = ANY(join_req) AND user_id = %s AND role = 'teacher';", (code,id,))
    if not x or x == None:
        return False
    return True

def validateMcq(data):
    try:
        if not(len(data.questions) == len(data.choices) and len(data.questions) == len(data.correct_answer)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Make sure questions, correct_answer, and choices are all the same length')
        for i in data.choices:
            if not (len(i) >= 2 and len(i) <= 4 and isinstance(i, list)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Make sure choices is a 2d array with the length of choices ranging from 2 to 4')
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

def validateTfq(data):
    try:
        if not(len(data.questions) == len(data.correct_answer)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid request make sure questions and correct_answer are the same length')
        for i in data.correct_answer:
            if not(isinstance(i, bool)):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Make sure the choices are booleans')
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

def validateCoding(data):
    try:
        if not(len(data.input) == len(data.output)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid request make sure input and output are the same length')
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

def checkCode(code):
    x = sqlQuery("SELECT * FROM class WHERE code = %s;",(str(code),))
    if not x or x == None:
        return False
    return True

def userInClass(id,code):
    x = sqlQuery("SELECT * FROM user_class WHERE user_id = %s AND code = %s;",(id,code,))
    if not x or x == None:
        return False
    return True

def assignmentInClass(id,code):
    w = sqlQuery("SELECT * FROM written WHERE assignment_id = %s AND code = %s;",(id,code,))
    f = sqlQuery("SELECT * FROM frq WHERE assignment_id = %s AND code = %s;",(id,code,))
    m = sqlQuery("SELECT * FROM mcq WHERE assignment_id = %s AND code = %s;",(id,code,))
    t = sqlQuery("SELECT * FROM tfq WHERE assignment_id = %s AND code = %s;",(id,code,))
    if not w and not f and not m and not t:
        return False
    return True

def verifyTeacher(id):
    x = sqlQuery("SELECT * FROM users WHERE user_id = %s AND role = 'teacher'",(id,))
    if not x or x == None:
        return False
    return True

def check_user(email: str):
    user = sqlQuery("SELECT * FROM users WHERE email = %s;",(email,))
    if not user:
        return False
    else:
        return True

def getUsername(id):
    user = sqlQuery("SELECT * FROM users WHERE user_is = %s;",(id,))
    if not user:
        return None
    else:
        return user["username"] # type: ignore

def postInClass(id,code):
    post = sqlQuery("SELECT * FROM posts WHERE post_id = %s AND code = %s;",(id,code,))
    if not post:
        return False
    else:
        return True

def checkPostOwner(user_id, post_id):
    post = sqlQuery("SELECT * FROM posts WHERE user_id = %s AND post_id = %s;",(user_id,post_id,))
    if not post:
        return False
    else:
        return True