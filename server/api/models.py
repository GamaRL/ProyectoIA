import enum
from sqlalchemy import Column, Enum, Integer, String

from .database import Base

# Files model

class FileType(enum.Enum):
  APRIORI = 0

class File(Base):
  __tablename__ = "files"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  file_token = Column(String, unique=True)
  algorithm = Column(Enum(FileType))
