from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Any
from ..schemas import user as UserSchemas
from ..controllers.user import ControllerUser
from ..database.database import getDB
from ..config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..security.security import Hasher, Token
from datetime import timedelta


userRouter = APIRouter()


@userRouter.get("/api/user/test", tags=["test"])
def testUser():
    return "Hello World Users"


@userRouter.post("/api/register", tags=["users"], response_model=UserSchemas.User, status_code=status.HTTP_201_CREATED)
async def register_user(*, user_in: UserSchemas.UserCreate, db: Session = Depends(getDB)) -> Any:
    user = await ControllerUser.fetch_by_username(db, _username=user_in.username)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exist")
    user_in.password = Hasher.password_encrypt(user_in.password)
    newUser = await ControllerUser.register(db, user=user_in)
    return newUser


@userRouter.post("/api/login", tags=["users"], status_code=status.HTTP_202_ACCEPTED)
async def login_user(*, user_in: UserSchemas.UserLogin, db: Session = Depends(getDB)):
    user = await ControllerUser.fetch_by_username(db, _username=user_in.username)
    if (not user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"type": "BAD", "message": "incorrect username or password"})
    confirm_password = Hasher.verify_password_hash(
        user_in.password, user.password)
    if not confirm_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"type": "BAD", "message": "incorrect username or password"})
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return JSONResponse({"access_token": Token.create_token(user.username, expires_delta=expires), "token_type": "bearer"})
