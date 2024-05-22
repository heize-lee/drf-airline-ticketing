# project/app/main.py
from fastapi import FastAPI
from app.routers import accounts

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

app.include_router(accounts.router)
