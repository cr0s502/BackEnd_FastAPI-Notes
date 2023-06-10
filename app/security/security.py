from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWSError, JWTError, jwt
from ..schemas.token import TokenData
from ..schemas.user import User
from ..config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from typing import Union, Optional, Any
from ..database.database import getDB
from ..controllers.user import ControllerUser


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:

    def password_encrypt(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password_hash(password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)


class Token:

    def create_token(data: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta is not None:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        encode = {"exp": expire, "sub": str(data)}
        jwt_encode = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        return jwt_encode

    def decode_token(token: str, db: Session) -> User:

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            token_data = TokenData(**payload)
        except (JWTError, JWSError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"type": "BAD", "message": "token missing or invalid"},
            )

        user = ControllerUser.fetch_by_username(db, _username=token_data.sub)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                "type": "BAD", "message": "token missing or invalid"})
        return user
