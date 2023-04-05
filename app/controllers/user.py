from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import user as UserSchemas
from ..models import user as UserModels
from datetime import datetime



class ControllerUser:
     
    async def register(db: Session, * , user: UserSchemas.UserCreate) -> UserModels.User:
       user_db = UserModels.User(name=user.name, lastname=user.lastname, username=user.username, createAt=datetime.now(), email=user.email, password=user.password)
       db.add(user_db)
       db.commit()
       db.refresh(user_db)
       return user_db
     
    async def fetch_by_id(db: Session, _id: int) -> UserModels.User :
      user = db.query(UserModels.User).filter_by( id == _id).first()
      return user
    
    async def fetch_by_username(db: Session, _username: str) -> UserModels.User:
      user = db.query(UserModels.User).filter( UserModels.User.username == _username).first()
      print(user)
      return user
    
    async def login(db: Session, user_in: UserSchemas.UserLogin):
      # user = db.query(UserModels.User).filter(UserModels.User.username == user_in.username).first()
      # if user in None:
      #   raise HTTPException(
      #       status_code=status.HTTP_400_BAD_REQUEST,
      #       detail="Incorrect email or password"
      #   )
      # confirm_password = Hasher.verify_password_hash(user_in, user.password)
      # if not confirm_password):
      #   raise HTTPException(status_code=400, detail="user or password incorrect")
      pass