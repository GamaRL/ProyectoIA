import enum
from sqlalchemy import TIMESTAMP, Column, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from .database import Base

# Files model

class FileType(enum.IntEnum):
  APRIORI = 0
  DISTANCES = 1


class File(Base):
  __tablename__ = "files"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  file_token = Column(String, unique=True)
  algorithm = Column(Enum(FileType))

class AssociationRuleExec(Base):
  __tablename__="exec_rules"
  id = Column(Integer, primary_key=True, index=True)
  file_id = Column(Integer, ForeignKey('files.id'))
  created_at = Column(TIMESTAMP, server_default=func.now())

class AssociationRule(Base):
  __tablename__ = "rules"
  id = Column(Integer, primary_key=True, index=True)
  exec_id = Column(Integer, ForeignKey('exec_rules.id'))
  antecedent = Column(String)
  consequent = Column(String)
  confidence = Column(Float)
  support = Column(Float)
  lift = Column(Float)


class StandarizationMethod(enum.IntEnum):
  NONE = 0
  SCALER = 1
  NORMALIZER = 2