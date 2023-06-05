import os
import numpy as np
import pandas as pd
from sklearn import model_selection

from sqlalchemy.orm import Session

from ..crud.file_service import get_file_by_id
from ..crud.helpers import __get_file_path__
from ..schemas import PrognosisSettingsData
from ..models import PrognosisSettings

def store_prognosis_params(db: Session, settings: PrognosisSettingsData):
  file = get_file_by_id(db, file_id = settings.file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not settings.contains_headers else 0)

  X = np.array(data[settings.predictor_variables])
  Y = np.array(data[[settings.prognosis_variable]])

  x_train_path =  os.path.join("/data/files", file.file_token + "_x_train.csv")
  y_train_path =  os.path.join("/data/files",file.file_token + "_y_train.csv")
  x_validation_path =  os.path.join("/data/files",file.file_token + "_x_validation.csv")
  y_validation_path =  os.path.join("/data/files",file.file_token + "_y_validation.csv")

  # print(settings)

  created_settings = PrognosisSettings(
    file_id=settings.file_id,
    predictor_variables=settings.predictor_variables,
    contains_headers=settings.contains_headers,
    prognosis_variable=settings.prognosis_variable,
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

  x_train, x_validation, y_train, y_validation = model_selection.train_test_split(X, Y, test_size=0.2, random_state=1234, shuffle = created_settings.shuffle)

  pd.DataFrame(x_train).to_csv(x_train_path)
  pd.DataFrame(y_train).to_csv(y_train_path)
  pd.DataFrame(x_validation).to_csv(x_validation_path)
  pd.DataFrame(y_validation).to_csv(y_validation_path)

  db.query(PrognosisSettings).filter(PrognosisSettings.file_id == settings.file_id).delete()
  db.add(created_settings)
  db.commit()
  db.refresh(created_settings)

  return PrognosisSettingsData(
    id=created_settings.id,
    file_id=created_settings.file_id,
    predictor_variables=created_settings.predictor_variables,
    contains_headers=created_settings.contains_headers,
    prognosis_variable=created_settings.prognosis_variable,
    test_size=created_settings.test_size,
    shuffle=created_settings.shuffle,
    use_forest=created_settings.use_forest,
    n_estimators=created_settings.n_estimators,
    max_depth=created_settings.max_depth,
    min_samples_split=created_settings.min_samples_split,
    min_samples_leaf=created_settings.min_samples_leaf
  )

def get_prog_settings_by_file_id(db: Session, file_id: int):
  return db.query(PrognosisSettings).filter(PrognosisSettings.file_id == file_id).first()

def get_prog_settings_data_by_file_id(db: Session, file_id: int):
  settings = get_prog_settings_by_file_id(db, file_id)

  if settings == None:
    return None

  return PrognosisSettingsData(
    id=settings.id,
    file_id=settings.file_id,
    predictor_variables=settings.predictor_variables,
    contains_headers=settings.contains_headers,
    prognosis_variable=settings.prognosis_variable,
    test_size=settings.test_size,
    shuffle=settings.shuffle,
    use_forest=settings.use_forest,
    n_estimators=settings.n_estimators,
    max_depth=settings.max_depth,
    min_samples_split=settings.min_samples_split,
    min_samples_leaf=settings.min_samples_leaf
  )