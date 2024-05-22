from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
