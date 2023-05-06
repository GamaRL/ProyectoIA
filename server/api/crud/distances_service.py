import os
import pandas as pd

from scipy.spatial import distance
from sqlalchemy.orm import Session

from ..crud.file_service import __get_file_path__, get_file_by_id
from ..crud.helpers import __normalize_matrix__, __scale_matrix__
from ..models import DistanceMetric, StandarizationMethod
from ..schemas import DistanceMatrixResponse


def get_distances_from_file_by_id(db: Session, file_id: int, download: bool, contains_headers: bool, columns: list[str], metric: DistanceMetric, standarization: StandarizationMethod = StandarizationMethod.NONE):
  file = get_file_by_id(db, file_id)
  path = __get_file_path__(file)
  content = pd.read_csv(path, header=None if not contains_headers else 0)[columns]

  if standarization == StandarizationMethod.NORMALIZER:
    content = __normalize_matrix__(content)
    content = pd.DataFrame(content)
  elif standarization == StandarizationMethod.SCALER:
    content = __scale_matrix__(content)
    content = pd.DataFrame(content)

  if metric == DistanceMetric.EUCLIDEAN:
    distances = distance.cdist(content, content, metric='euclidean')
  elif metric == DistanceMetric.MANHATTAN:
    distances = distance.cdist(content, content, metric='cityblock')
  elif metric == DistanceMetric.CHEVISHEV:
    distances = distance.cdist(content, content, metric='chebyshev')
  elif metric == DistanceMetric.MINKOWSKI:
    distances = distance.cdist(content, content, metric='minkowski', p=1.5)
  distances_matrix = pd.DataFrame(distances)

  if download:
    download_path = os.path.join("/tmp", file.file_token + ".csv")
    distances_matrix.to_csv(download_path)
    return str(download_path)

  return DistanceMatrixResponse(
    matrix = distances_matrix.round(4).stack().groupby(level=0).apply(list).to_list(),
  )
