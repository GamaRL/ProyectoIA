import os
import secrets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as ptl
from sklearn import linear_model, model_selection
from sklearn.base import accuracy_score
from sklearn.metrics import RocCurveDisplay

from sqlalchemy.orm import Session

from ..models import DistanceMetric, StandarizationMethod
from ..schemas import File
from .file_service import get_file_by_id, __get_file_path__
from .helpers import __get_file_path__, __normalize_matrix__, __scale_matrix__

def __create_roc_image__(file: File, classifier, x_validation, y_validation):
  RocCurveDisplay.from_estimator(classifier, x_validation, y_validation, name=file.name)

  filename = secrets.token_urlsafe(5) + ".png"
  image_path =  os.path.join("/tmp", filename)

  plt.savefig(image_path)

  return filename

def get_predict_info(db: Session, file_id: int, contains_headers, predictor_variables: list[str], class_variable: str, standarization: StandarizationMethod, metric: DistanceMetric, no_clusters: int):
  file = get_file_by_id(db, file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not contains_headers else 0)

  X = np.array(data[predictor_variables])
  Y = np.array(data[[class_variable]])

  x_train, x_validation, y_train, y_validation = model_selection.train_test_split(X, Y, test_size=0.2, random_state=1234, shuffle = True)

  classifier = linear_model.LogisticRegression()

  classifier.fit(x_train, y_train)

  y_classified = classifier.predict(x_validation)

  model_accuracy_score = accuracy_score(y_validation, y_classified)
  model_roc_img = __create_roc_image__(file, classifier, x_validation, y_validation)