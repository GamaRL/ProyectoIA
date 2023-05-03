from datetime import datetime
from pydantic import BaseModel

from .models import FileType

class AssociationRuleExec(BaseModel):
  id: int
  file_id: int
  created_at: datetime

  class Config:
    orm_mode = True

class AssociationRuleRow(BaseModel):
  antecedent: str
  consequent: str
  confidence: float
  support: float
  lift: float

  def __lt__ (self, v):
    return self.lift - v.lift

class AssociationRule(AssociationRuleRow):
  id: int
  exec_id: int

  class Config:
    orm_mode = True

class FileBase(BaseModel):
  name: str
  file_token: str
  algorithm: FileType

class File(FileBase):
  id: int
  rules: list[AssociationRule]

  class Config:
    orm_mode = True

class FileContent(BaseModel):
  headers: list[str] = None
  head: list[list[str]]
  tail: list[list[str]]

class StatisticsRow(BaseModel):
  item: str
  frequency: int
  relative: float

class AssociationRuleExecResponse(BaseModel):
  id: int
  created_at: datetime

  rules: list[AssociationRuleRow]
