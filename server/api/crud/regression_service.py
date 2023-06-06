import os
import secrets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as ptl
from sklearn import linear_model, model_selection
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import RocCurveDisplay

from sqlalchemy.orm import Session

from ..models import RegressionSettings
from ..schemas import File, RegressionExecResponse, RegressionSettingsData, RegressionInfoResponse
from .file_service import get_file_by_id, __get_file_path__
from .helpers import __get_file_path__, __normalize_matrix__, __scale_matrix__, __filter_multiple_columns__

def __create_roc_image__(file: File, classifier, x_validation, y_validation):
  RocCurveDisplay.from_estimator(classifier, x_validation, y_validation, name=file.name)

  filename = secrets.token_urlsafe(5) + ".png"
  image_path =  os.path.join("/tmp", filename)

  plt.savefig(image_path)

  return filename

def store_regression_params(db: Session, settings: RegressionSettingsData):
  file = get_file_by_id(db, file_id = settings.file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not settings.contains_headers else 0)

  X = np.array(data[settings.predictor_variables])
  Y = np.array(data[[settings.class_variable]])

  x_train_path =  os.path.join("/data/files", file.file_token + "_x_train.csv")
  y_train_path =  os.path.join("/data/files",file.file_token + "_y_train.csv")
  x_validation_path =  os.path.join("/data/files",file.file_token + "_x_validation.csv")
  y_validation_path =  os.path.join("/data/files",file.file_token + "_y_validation.csv")

  created_settings = RegressionSettings(
    file_id=settings.file_id,
    predictor_variables=settings.predictor_variables,
    contains_headers=settings.contains_headers,
    class_variable=settings.class_variable,
    test_size=settings.test_size,
    shuffle=settings.shuffle,

    x_train_path=x_train_path,
    x_validation_path=x_validation_path,
    y_train_path=y_train_path,
    y_validation_path=y_validation_path
  )

  x_train, x_validation, y_train, y_validation = model_selection.train_test_split(X, Y, test_size=0.2, random_state=1234, shuffle = True)

  pd.DataFrame(x_train).to_csv(x_train_path)
  pd.DataFrame(y_train).to_csv(y_train_path)
  pd.DataFrame(x_validation).to_csv(x_validation_path)
  pd.DataFrame(y_validation).to_csv(y_validation_path)

  db.query(RegressionSettings).filter(RegressionSettings.file_id == settings.file_id).delete()
  db.add(created_settings)
  db.commit()
  db.refresh(created_settings)

  return RegressionSettingsData(
    file_id=created_settings.file_id,
    predictor_variables=created_settings.predictor_variables,
    contains_headers=created_settings.contains_headers,
    class_variable=created_settings.class_variable,
    test_size=created_settings.test_size,
    shuffle=created_settings.shuffle,
  )

def get_settings_by_file_id(db: Session, file_id: int):
  return db.query(RegressionSettings).filter(RegressionSettings.file_id == file_id).first()

def get_regr_settings_data_by_file_id(db: Session, file_id: int):
  settings = get_settings_by_file_id(db, file_id)

  if settings == None:
    return None

  return RegressionSettingsData(
    id=settings.id,
    file_id=settings.file_id,
    predictor_variables=settings.predictor_variables,
    contains_headers=settings.contains_headers,
    class_variable=settings.class_variable,
    test_size=settings.test_size,
    shuffle=settings.shuffle,
  )

def __load_train_data__(settings: RegressionSettings):
  x_train = pd.read_csv(settings.x_train_path, index_col=0).to_numpy()
  y_train = pd.read_csv(settings.y_train_path, index_col=0).to_numpy()
  x_validation = pd.read_csv(settings.x_validation_path, index_col=0).to_numpy()
  y_validation = pd.read_csv(settings.y_validation_path, index_col=0).to_numpy()

  return (x_train, x_validation, y_train, y_validation)

def get_valid_class_variables(db: Session, file_id: int):

  file = get_file_by_id(db, file_id = file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not True else 0)

  return __filter_multiple_columns__(data, 2)

def get_predict_info(db: Session, file_id: int):

  file = get_file_by_id(db, file_id)
  settings = get_settings_by_file_id(db, file_id)

  x_train, x_validation, y_train, y_validation = __load_train_data__(settings)

  classifier = linear_model.LogisticRegression()
  classifier.fit(x_train, y_train.ravel())

  y_classified = classifier.predict(x_validation)

  matrix = pd.crosstab(
    y_validation.ravel(),
    y_classified,
    rownames=["Reality"],
    colnames=["Classification"]
  )

  model_accuracy_score = accuracy_score(y_validation, y_classified)
  model_roc_img = __create_roc_image__(file, classifier, x_validation, y_validation)

  return RegressionInfoResponse(
    file_id=settings.file_id,
    accuracy_score=model_accuracy_score,
    roc_image_file=model_roc_img,
    crosstab=matrix.to_numpy().tolist(),
    report=classification_report(y_validation, y_classified, output_dict=True)
  )

def get_prediction(db: Session, file_id: int, row_data = dict[str, float]):

  settings = get_settings_by_file_id(db, file_id)

  x_train, x_validation, y_train, y_validation = __load_train_data__(settings)

  classifier = linear_model.LogisticRegression()
  classifier.fit(x_train, y_train.ravel())

  x_data = pd.DataFrame(row_data, index=[0]).to_numpy()
  y_classified = classifier.predict(x_data)
  probability = classifier.predict_proba(x_data)

  return RegressionExecResponse(
    label=str(y_classified[0]),
    probability_0=probability[0][0],
    probability_1=probability[0][1]
  )