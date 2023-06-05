import enum
from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, Float, ForeignKey, Integer, String, func

from .database import Base

# Files model

class FileType(enum.IntEnum):
  APRIORI = 0
  DISTANCES = 1
  CLUSTERING = 2
  LOGISTIC_REGRESSION = 3
  CLASSIFICATION = 4
  PROGNOSIS = 5


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

class DistanceMetric(enum.IntEnum):
  EUCLIDEAN = 0
  MANHATTAN = 1
  CHEVISHEV = 2
  MINKOWSKI = 3

class DimensionalityReductionType(enum.IntEnum):
  CORRELATION = 0
  PCA = 1

class RegressionSettings(Base):
  __tablename__ = "regression_settings"
  id = Column(Integer, primary_key=True, index=True)
  file_id = Column(Integer, ForeignKey('files.id'))
  contains_headers = Column(Boolean)
  _predictor_variables = Column(String)
  class_variable = Column(String)
  test_size = Column(Float)
  shuffle = Column(Boolean)
  x_train_path = Column(String)
  y_train_path = Column(String)
  x_validation_path = Column(String)
  y_validation_path = Column(String)

  @property
  def predictor_variables(self):
    return self._predictor_variables.split(';')

  @predictor_variables.setter
  def predictor_variables(self, value: list[str]):
    self._predictor_variables = ';'.join(value)

class PrognosisSettings(Base):
  __tablename__ = "prognosis_settings"
  id = Column(Integer, primary_key=True, index=True)
  file_id = Column(Integer, ForeignKey('files.id'))
  contains_headers = Column(Boolean)
  _predictor_variables = Column(String)
  prognosis_variable = Column(String)
  test_size = Column(Float)
  shuffle = Column(Boolean)
  use_forest = Column(Boolean)
  n_estimators = Column(Integer)
  max_depth = Column(Integer)
  min_samples_split = Column(Integer)
  min_samples_leaf = Column(Integer)
  x_train_path = Column(String)
  y_train_path = Column(String)
  x_validation_path = Column(String)
  y_validation_path = Column(String)

  @property
  def predictor_variables(self):
    return self._predictor_variables.split(';')

  @predictor_variables.setter
  def predictor_variables(self, value: list[str]):
    self._predictor_variables = ';'.join(value)