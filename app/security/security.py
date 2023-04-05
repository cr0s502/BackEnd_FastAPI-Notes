from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from ..schemas.token import Token, TokenData
from ..schemas.user import User
from ..config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from typing import Union, Any, Optional
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
      
    def decode_token(db: Session = Depends(getDB), token: str = Depends()) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms[ALGORITHM])
            token_data = TokenData(**payload)
        except (JWTError, ValidationError):
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            )
        user = ControllerUser.fetch_by_username(db, _username=token_data.sub)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user