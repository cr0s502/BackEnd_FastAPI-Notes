
from datetime import datetime
from pydantic import BaseModel
from .note import Note

class UserBase(BaseModel):
    name: str
    lastname: str
    email: str
    username: str
    password: str
    
class UserCreate(UserBase):
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
    