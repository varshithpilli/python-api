from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(user_creds: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    return {"token": "example token"}