from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from ..database.database import Base
from .note import Note


class User(Base):
    __tablename__: str = "users"

    id = Column(Integer, primary_key=True,  index=True)
    name = Column(VARCHAR(10), nullable=False)
    lastname = Column(VARCHAR(15), nullable=False)
    username = Column(VARCHAR(15), nullable=False, index=True, unique=True)
    email = Column(VARCHAR(30), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    createAt = Column(DateTime, nullable=False)
    notes = relationship(
        "Note", primaryjoin="User.id == Note.user_id", cascade="all, delete-orphan")

    # def __repr__(self):
    #     return "User(id=%s, name=%s, lastname=%s, username=%s, email=%s, createAt=%s, notes=%s)" % (self.id, self.name, self.lastname, self.lastname, self.email, self.createAt, self.notes)
