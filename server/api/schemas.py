from pydantic import BaseModel

from .models import FileType


class FileBase(BaseModel):
  name: str
  file_token: str
  algorithm: FileType

class File(FileBase):
  id: int

  class Config:
    orm_mode = True

class FileContent(BaseModel):
  head: list[list[str]]
  tail: list[list[str]]

class StatisticsRow(BaseModel):
  item: str
  frequency: int
  relative: float

class AssociationRuleRow(BaseModel):
  antecedent: str
  consequent: str
  confidence: float
  support: float
  lift: float

  def __lt__ (self, v):
    return self.lift - v.lift