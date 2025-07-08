from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .schemas import auth_schemas
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
load_dotenv()


#secret_key
#algorithm - hs256
#Expiration time

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM) # type: ignore

    return token

def verify_access_token(token:str, credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        id = str(payload.get("user_id"))
        if not id:
            raise credentials_exeption
        token_data = auth_schemas.TokenData(id=id)
    except JWTError as e:
        raise credentials_exeption
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token, credentials_exeption=credentials_exeption)
