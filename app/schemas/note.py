from pydantic import BaseModel
import datetime
# from pydantic.schema import Optional


class NoteBase(BaseModel):
    content: str
    important: bool | None = None


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    user_id: int
    createAt: str = datetime.datetime

    class Config:
        orm_mode = True
