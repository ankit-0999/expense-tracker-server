from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr


class User(Document):
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    name: str = ""

    class Settings:
        name = "users"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str = ""


class UserLogin(BaseModel):
    email: EmailStr
    password: str
