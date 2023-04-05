from pydantic import BaseModel

class NoteBase(BaseModel):
    content: str
    important: bool | None = None
  
class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    user_id: int
  
    class Config:
      orm_mode = True