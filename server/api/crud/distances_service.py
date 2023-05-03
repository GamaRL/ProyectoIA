import pandas as pd

from scipy.spatial import distance
from sqlalchemy.orm import Session

from ..crud.file_service import _get_file_path, get_file_by_id
from ..crud.helpers import __normalize_matrix__, __scale_matrix__
from ..models import StandarizationMethod
from ..schemas import DistanceMatrixResponse

def get_distances_from_file_by_id(db: Session, file_id: int, contains_headers: bool, columns: list[str], method: StandarizationMethod = StandarizationMethod.NONE):
  file = get_file_by_id(db, file_id)
  path = _get_file_path(file)
  content = pd.read_csv(path, header=None if not contains_headers else 0)[columns]

  if method == StandarizationMethod.NORMALIZER:
    content = __normalize_matrix__(content)
    content = pd.DataFrame(content)
  elif method == StandarizationMethod.SCALER:
    content = __scale_matrix__(content)
    content = pd.DataFrame(content)

  distances = distance.cdist(content, content, metric='euclidean')
  distances_matrix = pd.DataFrame(distances)

  return DistanceMatrixResponse(
    matrix = distances_matrix.round(2).stack().groupby(level=0).apply(list).to_list(),
  )
