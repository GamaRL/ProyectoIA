import os
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sqlalchemy.orm import Session

from .file_service import get_file_by_id
from .helpers import __get_file_path__
from ..schemas import ClassificationExecResponse, ClassificationSettingsData
from ..models import ClassificationSettings
from .helpers import __get_file_path__, __normalize_matrix__, __scale_matrix__, __filter_multiple_columns__

def store_classification_params(db: Session, settings: ClassificationSettingsData):
  file = get_file_by_id(db, file_id = settings.file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not settings.contains_headers else 0)

  X = np.array(data[settings.predictor_variables])
  Y = np.array(data[[settings.class_variable]])

  x_train_path =  os.path.join("/data/files", file.file_token + "_x_train.csv")
  y_train_path =  os.path.join("/data/files",file.file_token + "_y_train.csv")
  x_validation_path =  os.path.join("/data/files",file.file_token + "_x_validation.csv")
  y_validation_path =  os.path.join("/data/files",file.file_token + "_y_validation.csv")

  created_settings = ClassificationSettings(
    file_id=settings.file_id,
    predictor_variables=settings.predictor_variables,
    contains_headers=settings.contains_headers,
    class_variable=settings.class_variable,
    test_size=settings.test_size,
    shuffle=settings.shuffle,
    use_forest=settings.use_forest,
    n_estimators=settings.n_estimators,
    max_depth=settings.max_depth,
    min_samples_split=settings.min_samples_split,
    min_samples_leaf=settings.min_samples_leaf,

    x_train_path=x_train_path,
    x_validation_path=x_validation_path,
    y_train_path=y_train_path,
    y_validation_path=y_validation_path
  )

  x_train, x_validation, y_train, y_validation = model_selection.train_test_split(
    X,
    Y,
    test_size=created_settings.test_size,
    random_state=0,
    shuffle = created_settings.shuffle)

  pd.DataFrame(x_train).to_csv(x_train_path)
  pd.DataFrame(y_train).to_csv(y_train_path)
  pd.DataFrame(x_validation).to_csv(x_validation_path)
  pd.DataFrame(y_validation).to_csv(y_validation_path)

  db.query(ClassificationSettings).filter(ClassificationSettings.file_id == settings.file_id).delete()
  db.add(created_settings)
  db.commit()
  db.refresh(created_settings)

  return ClassificationSettingsData(
    id=created_settings.id,
    file_id=created_settings.file_id,
    predictor_variables=created_settings.predictor_variables,
    contains_headers=created_settings.contains_headers,
    class_variable=created_settings.class_variable,
    test_size=created_settings.test_size,
    shuffle=created_settings.shuffle,
    use_forest=created_settings.use_forest,
    n_estimators=created_settings.n_estimators,
    max_depth=created_settings.max_depth,
    min_samples_split=created_settings.min_samples_split,
    min_samples_leaf=created_settings.min_samples_leaf
  )

def __load_train_data__(settings: ClassificationSettings):
  x_train = pd.read_csv(settings.x_train_path, index_col=0).to_numpy()
  y_train = pd.read_csv(settings.y_train_path, index_col=0).to_numpy()
  x_validation = pd.read_csv(settings.x_validation_path, index_col=0).to_numpy()
  y_validation = pd.read_csv(settings.y_validation_path, index_col=0).to_numpy()

  return (x_train, x_validation, y_train, y_validation)

def get_classification_settings_by_file_id(db: Session, file_id: int):
  return db.query(ClassificationSettings).filter(ClassificationSettings.file_id == file_id).first()

def get_class_settings_data_by_file_id(db: Session, file_id: int):
  settings = get_classification_settings_by_file_id(db, file_id)

  if settings == None:
    return None

  return ClassificationSettingsData(
    id=settings.id,
    file_id=settings.file_id,
    predictor_variables=settings.predictor_variables,
    contains_headers=settings.contains_headers,
    class_variable=settings.class_variable,
    test_size=settings.test_size,
    shuffle=settings.shuffle,
    use_forest=settings.use_forest,
    n_estimators=settings.n_estimators,
    max_depth=settings.max_depth,
    min_samples_split=settings.min_samples_split,
    min_samples_leaf=settings.min_samples_leaf
  )

def get_classification(db: Session, file_id: int, row_data = dict[str, float]):

  settings = get_classification_settings_by_file_id(db, file_id)

  x_train, _, y_train, _ = __load_train_data__(settings)

  if settings.use_forest:
    classifier = RandomForestClassifier(
      n_estimators=settings.n_estimators,
      max_depth=settings.max_depth,
      min_samples_leaf=settings.min_samples_leaf,
      min_samples_split=settings.min_samples_split,
      random_state=0
    )
  else:
    classifier = DecisionTreeClassifier(
      max_depth=settings.max_depth,
      min_samples_leaf=settings.min_samples_leaf,
      min_samples_split=settings.min_samples_split,
      random_state=0
    )

  classifier.fit(x_train, y_train.ravel())

  x_data = pd.DataFrame(row_data, index=[0]).to_numpy()

  y_classified = classifier.predict(x_data)

  return ClassificationExecResponse(
    label=str(y_classified[0]),
    class_variable=str(settings.class_variable)
  )

def get_classification_info(db: Session, file_id: int):

  settings = get_classification_settings_by_file_id(db, file_id)

  x_train, x_validation, y_train, y_validation = __load_train_data__(settings)

  if settings.use_forest:
    classifier = RandomForestClassifier(
      n_estimators=settings.n_estimators,
      max_depth=settings.max_depth,
      min_samples_leaf=settings.min_samples_leaf,
      min_samples_split=settings.min_samples_split,
      random_state=0
    )
  else:
    classifier = DecisionTreeClassifier(
      max_depth=settings.max_depth,
      min_samples_leaf=settings.min_samples_leaf,
      min_samples_split=settings.min_samples_split,
      random_state=0
    )

  classifier.fit(x_train, y_train.ravel())
  y_classify = classifier.predict(x_validation)

  importance_values = classifier.feature_importances_.tolist()
  importance = dict(zip(settings.predictor_variables, importance_values))

  return None

def get_multiple_class_variables(db: Session, file_id: int):

  file = get_file_by_id(db, file_id = file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not True else 0)

  return __filter_multiple_columns__(data, 5)
