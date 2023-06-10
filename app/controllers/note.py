from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..schemas import note as NoteSchemas
from ..models import note as NoteModels
from ..schemas import token
from ..security.security import Token
from datetime import datetime


class ControllerNote:

    async def create_note(db: Session, note: NoteSchemas.NoteCreate, token: str) -> NoteSchemas.Note:
        user = await Token.decode_token(token, db)
        newNote = NoteModels.Note(
            content=note.content, important=note.important, createAt=datetime.now(), user_id=user.id)
        db.add(newNote)
        db.commit()
        db.refresh(newNote)
        return newNote

    async def get_notes(db: Session, token: str) -> list[NoteSchemas.Note]:
        user = await Token.decode_token(token, db)
        notes = db.query(NoteModels.Note).filter(
            NoteModels.Note.user_id == user.id).all()
        if notes is None:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, detail={"type": "GOOD", "message": "Don't have notes"})
        return notes

    async def note_by_id(db: Session, _id: int, token: str) -> NoteSchemas.Note:
        user = await Token.decode_token(token, db)
        note = db.query(NoteModels.Note).where(NoteModels.Note.id == _id).where(
            NoteModels.Note.user_id == user.id).first()
        return note

    async def update_note(db: Session, _id: int, note: NoteSchemas.NoteCreate, token: str) -> NoteSchemas.Note:
        user = await Token.decode_token(token, db)
        db.query(NoteModels.Note).where(NoteModels.Note.id == _id).where(
            NoteModels.Note.user_id == user.id).update({"content": note.content, "important": note.important})
        db.commit()
        noteUpdate = await ControllerNote.note_by_id(db, _id, token)
        return noteUpdate

    # update(user_table).values(fullname="Username: " + user_table.c.name)

    async def delete_note(db: Session, _id: int, token: str):
        note = await ControllerNote.note_by_id(db, _id, token)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={"type": "BAD", "message": f"note with id {_id} not found"})
        try:
            db.delete(note)
            db.commit()
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={"type": "GOOD", "message": "error for eliminate note"})
        return True
