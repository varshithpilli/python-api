from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from . import schemas, database, models
import os
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

key = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM")
exp_time = int(os.getenv("EXPIRY_MINUTES"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=exp_time)
    print(datetime.now(timezone.utc))
    print(expire)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, key, algorithm=algo)

    return encoded_jwt

def verify_access_token(token: str, creds_exception):
    try:
        payload = jwt.decode(token, key, algorithms=algo)

        id: int = payload.get("user_id")

        if id is None:
            raise creds_exception
        
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise creds_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    creds_exception = HTTPException(status_code=401,
                                    detail=f"Could not validate credentials",
                                    headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, creds_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user