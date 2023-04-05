
from ..config.config import ENGINE_DATABASE, USER_DATABASE, PASSWORD_DATABASE, HOST_DATABASE, PORT_DATABASE, NAME_DATABASE
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL =  "mysql+pymysql://root:Cross19950502@127.0.0.1:3306/notes"
#f"{ENGINE_DATABASE}://{USER_DATABASE}:{PASSWORD_DATABASE}@{HOST_DATABASE}:{PORT_DATABASE}/{NAME_DATABASE}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def getDB():
    db = SessionLocal()
    try:
      yield db
    finally:
      db.close()