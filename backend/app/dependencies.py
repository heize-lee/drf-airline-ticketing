from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app import crud, schemas, auth
from app.database import SessionLocal
from app.auth import get_current_user as auth_get_current_user
from app.models import User
from app.schemas import TokenData
from app.config import settings
from app.auth import oauth2_scheme
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app import crud, schemas, auth
from app.database import SessionLocal
from app.auth import get_user_from_token
from app.schemas import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return get_user_from_token(db, token)