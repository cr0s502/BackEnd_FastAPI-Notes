from sqlalchemy import Column, ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.dialects.mysql import VARCHAR
from ..database.database import Base

print(type(Base))
class Note(Base):
  __tablename__ = "notes"
  id = Column(Integer, primary_key=True, index=True)
  content = Column(VARCHAR(255), nullable=False)
  important = Column(Boolean, default=False)
  createAt = Column(DateTime, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  
  def __repr__(self):
      return "NoteModel(id=%s, content=%s, important=%s)" % (self.id, self.content, self.important)
  