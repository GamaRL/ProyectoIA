import os
import secrets
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.calibration import label_binarize
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import RocCurveDisplay, auc, classification_report, roc_curve

from sqlalchemy.orm import Session

from .file_service import get_file_by_id
from .helpers import __get_file_path__
from ..schemas import ClassificationExecResponse, ClassificationInfoResponse, ClassificationSettingsData, File
from ..models import ClassificationSettings
from .helpers import __get_file_path__, __normalize_matrix__, __scale_matrix__, __filter_multiple_columns__, __create_roc_image__

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

def __create_roc_image__(settings, classifier, x_validation, y_validation):
  classes = pd.DataFrame(y_validation)[0].unique().tolist()

  y_score = classifier.predict_proba(x_validation)
  y_test_bin = label_binarize(y_validation, classes=classes)

  colors = ['blue', 'orange', 'lime', 'pink', 'cyan']

  plt.figure(figsize=[12, 6])
  if len(classes) > 2:
    for i in range(len(classes)):
      fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
      plt.plot(fpr, tpr, color=colors[i], lw=1)
  else:
    fpr, tpr, _ = roc_curve(y_test_bin[:, 0], y_score[:, 0])
    plt.plot(fpr, tpr, color='blue', lw=1)

  plt.plot([0, 1], [0, 1], color='lightgray', lw=1, linestyle='--')
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.05])
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.title('Score')

  filename = secrets.token_urlsafe(5) + ".png"
  image_path =  os.path.join("/tmp", filename)

  plt.savefig(image_path)

  return filename

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

  matrix = pd.crosstab(
    y_validation.ravel(),
    y_classify,
    rownames=["Reality"],
    colnames=["Classification"]
  )

  importance_values = classifier.feature_importances_.tolist()
  importance = dict(zip(settings.predictor_variables, importance_values))

  report = classification_report(y_validation, y_classify, output_dict=True)
  report.pop("accuracy")

  roc_image_file = __create_roc_image__(settings, classifier, x_validation, y_validation)

  crosstab = dict()

  for k in matrix.columns.to_list():
    crosstab[k] = matrix[k].tolist()
  
  return ClassificationInfoResponse(
    file_id=settings.file_id,
    criterio=classifier.criterion,
    importance=importance,
    score=classifier.score(x_validation, y_validation),
    crosstab=crosstab,
    report=report,
    roc_image_file=roc_image_file
  )


def get_multiple_class_variables(db: Session, file_id: int):

  file = get_file_by_id(db, file_id = file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not True else 0)

  return __filter_multiple_columns__(data, 5)