# # project/app/routers/accounts.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.schemas import UserCreate, User, Token
# from app.crud import create_user, get_user_by_email, delete_user
# from app.auth import create_access_token, verify_password
# from app.database import get_db

# router = APIRouter(
#     prefix="/accounts",
#     tags=["accounts"],
# )

# @router.post("/signup", response_model=User)
# def signup(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = get_user_by_email(db, user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return create_user(db, user)

# @router.post("/login", response_model=Token)
# def login(form_data: UserCreate, db: Session = Depends(get_db)):
#     user = get_user_by_email(db, form_data.email)
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     if not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.delete("/delete/{uid}", response_model=User)
# def delete_user_account(uid: int, db: Session = Depends(get_db)):
#     user = delete_user(db, uid)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.post("/change-password")
# def change_password(old_password: str, new_password: str, db: Session = Depends(get_db)):
#     # 비밀번호 변경 로직 추가 필요
#     pass

# project/app/routers/accounts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas import UserCreate, User, Token
from app.crud import create_user, get_user_by_email, delete_user
from app.auth import create_access_token, verify_password, decode_access_token
from app.database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="accounts/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/signup", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.delete("/delete/{uid}", response_model=User)
def delete_user_account(uid: int, db: Session = Depends(get_db)):
    user = delete_user(db, uid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/change-password")
def change_password(old_password: str, new_password: str, db: Session = Depends(get_db)):
    # 비밀번호 변경 로직 추가 필요
    pass
