from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

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