# project/app/models.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)  # 필드 이름 확인
    lastName = Column(String, index=True)   # 필드 이름 확인
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

