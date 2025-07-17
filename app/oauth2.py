from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from . import schemas
import os
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

key = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM")
exp_time = int(os.getenv("EXPIRY_MINUTES"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=exp_time)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, key, algorithm=algo)

    return encoded_jwt

def verify_access_token(token: str, creds_exception):
    try:
        payload = jwt.decode(token, key, algorithms=algo)

        id: str = payload.get("user_id")

        if id is None:
            raise creds_exception
        
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise creds_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    creds_exception = HTTPException(status_code=401,
                                    detail=f"Could not validate credentials",
                                    headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, creds_exception)