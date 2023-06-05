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

class CorrelationAnalysis(BaseModel):
  map_filename: str
  strong_corrs: list[list[str, str]]

class StatisticsRow(BaseModel):
  item: str
  frequency: int
  relative: float

class AssociationRuleExecResponse(BaseModel):
  id: int
  created_at: datetime

  rules: list[AssociationRuleRow]

class DistanceMatrixResponse(BaseModel):
  matrix: list[list[float]]

class AgglomerativeClusterResponse(BaseModel):
  id: int
  properties: dict[str, float]
  cluster: int

class RegressionSettingsData(BaseModel):
  id: int|None
  file_id: int
  contains_headers: bool
  predictor_variables: list[str]
  class_variable: str
  test_size: float
  shuffle: bool

  class Config:
    orm_mode = True

class PrognosisSettingsData(BaseModel):
  id: int|None
  file_id: int
  contains_headers: bool
  predictor_variables: list[str]
  prognosis_variable: str
  test_size: float
  shuffle: bool
  use_forest: bool
  n_estimators: int
  max_depth: int
  min_samples_split: int
  min_samples_leaf: int

  class Config:
    orm_mode = True

class RegressionInfoResponse(BaseModel):
  file_id: int
  accuracy_score: float
  roc_image_file: str
  crosstab: list[list[float]]
  report: dict

class RegressionExecResponse(BaseModel):
  label: str
  probability_0: float
  probability_1: float

class PrognosisExecResponse(BaseModel):
  value: float