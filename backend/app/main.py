from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas, crud, auth
from app.routers import accounts

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정 추가
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts.router)
# app.include_router(flights.router)  # include the flights router

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup", response_model=schemas.User)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("Received user data:", user)  # 데이터를 출력하여 확인
    db_user = crud.create_user(db, user)
    return db_user

@app.post("/login")
async def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"message": "Login successful"}

@app.get("/")
def read_root():
    return {"Hello": "World"}
