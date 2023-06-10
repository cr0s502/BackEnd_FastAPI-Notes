from sqlalchemy import Column, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.dialects.mysql import VARCHAR
from ..database.database import Base


class Note(Base):
    __tablename__: str = "notes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(VARCHAR(255), nullable=False)
    important = Column(Boolean, default=False)
    createAt = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # def __repr__(self):
    #     return "Note(id=%s, content=%s, important=%s, createAt=%s, user_id=%s)" % (self.id, self.content, self.important, self.createAt, self.user_id)
