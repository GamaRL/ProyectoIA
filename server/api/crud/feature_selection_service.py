import os
import secrets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sqlalchemy.orm import Session

from .file_service import get_file_by_id, get_file_headers
from ..schemas import CorrelationAnalysis
from ..models import StandarizationMethod
from .helpers import __get_file_path__

def get_correlation_matrix(db: Session, file_id: int, contains_headers: bool, standarization: StandarizationMethod):
  columns: list[str] = get_file_headers(db, file_id, contains_headers)

  file = get_file_by_id(db, file_id)
  path = __get_file_path__(file)
  content = pd.read_csv(path, header=None if not contains_headers else 0)[columns]

  correlation_matrix = content.corr(method='pearson')
  correlation_values = pd.DataFrame(
    np.tril(correlation_matrix, -1),
    columns=correlation_matrix.columns.tolist(),
    index=correlation_matrix.index.tolist()
  )

  strong_corrs = []
  for col in correlation_matrix.columns.to_list():
      for idx in correlation_values.index[abs(correlation_values[col]) > 0.75].tolist():
        if [idx, col] not in strong_corrs:
           strong_corrs.append([col, idx])

  plt.figure(figsize=(15,12))
  MatrizInf = np.triu(correlation_matrix)
  sns.heatmap(correlation_matrix, cmap='RdBu_r', annot=True, mask=MatrizInf, vmin=-1, vmax=1)

  filename = secrets.token_urlsafe(5) + ".png"
  image_path =  os.path.join("/tmp", filename)

  plt.savefig(image_path)

  return CorrelationAnalysis(map_filename=filename, strong_corrs=strong_corrs)
