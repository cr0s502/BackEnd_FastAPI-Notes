
from datetime import datetime
from pydantic import BaseModel, EmailStr
from .note import Note


class UserBase(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    pass


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    createAt: datetime | None = None
    notes: list[Note] = []

    class Config:
        orm_mode = True
