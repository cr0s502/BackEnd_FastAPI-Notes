from fastapi import APIRouter, status, Depends, HTTPException, Header, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..controllers.note import ControllerNote
from ..database.database import getDB
from ..schemas import note as NoteSchemas
from ..models import note as NoteModels
from typing import Any
from fastapi.security import OAuth2PasswordBearer


noteRouter = APIRouter()


@noteRouter.get("/api/note/test", tags=["test"])
def testNote():
    return "Hello World Notes"


@noteRouter.post("/api/note", tags=["notes"], response_model=NoteSchemas.Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteSchemas.NoteCreate, authorization: str = Header(...), db: Session = Depends(getDB)) -> Any:

    if authorization.split()[0] != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={"type": "BAD", "message": "Invalid authentication scheme"})

    token = authorization.split()[1]
    newNota = await ControllerNote.create_note(db, note, token)
    return newNota


@noteRouter.get("/api/note", tags=["notes"], response_model=list[NoteSchemas.Note], status_code=status.HTTP_200_OK)
async def get_all_notes(authorization: str = Header(...), db: Session = Depends(getDB)) -> Any:

    if authorization.split()[0] != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={"type": "BAD", "message": "Invalid authentication scheme"})

    token = authorization.split()[1]
    notes = await ControllerNote.get_notes(db, token)
    return notes


@noteRouter.get("/api/note/{id}", tags=["notes"], response_model=NoteSchemas.Note, status_code=status.HTTP_200_OK)
async def get_note_by_id(id: int, authorization: str = Header(...), db: Session = Depends(getDB)) -> Any:
    if authorization.split()[0] != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={"type": "BAD", "message": "Invalid authentication scheme"})

    token = authorization.split()[1]
    note = await ControllerNote.note_by_id(db, id, token)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={
                "type": "BAD", "message": f"note with id {id} not found"}
        )
    return note


@noteRouter.put("/api/note/{id}", tags=["notes"], response_model=NoteSchemas.Note, status_code=status.HTTP_200_OK)
async def update_note(note: NoteSchemas.NoteCreate, id: int, authorization: str = Header(...), db: Session = Depends(getDB)) -> Any:

    if authorization.split()[0] != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={"type": "BAD", "message": "Invalid authentication scheme"})

    token = authorization.split()[1]
    note = await ControllerNote.update_note(db, id, note, token)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={
                "type": "BAD", "message": f"note with {id} not found"}
        )
    return note


@noteRouter.delete("/api/note/{id}", tags=["notes"], status_code=status.HTTP_200_OK)
async def delete_note(id: int, authorization: str = Header(...), db: Session = Depends(getDB)) -> Any:
    if authorization.split()[0] != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={"type": "BAD", "message": "Invalid authentication scheme"})

    token = authorization.split()[1]
    valid_delete = await ControllerNote.delete_note(db, id, token)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"type": "GOOD", "message": "Note Eliminated"}, media_type="application/json")
