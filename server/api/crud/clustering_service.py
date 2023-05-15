import os
import secrets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy.orm import Session
from sklearn.cluster import AgglomerativeClustering

from ..models import StandarizationMethod
from ..schemas import AgglomerativeClusterResponse, CorrelationAnalysis
from .file_service import get_file_by_id, __get_file_path__, get_file_headers
from .helpers import __get_file_path__, __normalize_matrix__, __scale_matrix__

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
      for idx in correlation_values.index[correlation_values[col] > 0.75].tolist():
        if [idx, col] not in strong_corrs:
           strong_corrs.append([col, idx])

  plt.figure(figsize=(15,12))
  MatrizInf = np.triu(correlation_matrix)
  sns.heatmap(correlation_matrix, cmap='RdBu_r', annot=True, mask=MatrizInf)

  filename = secrets.token_urlsafe(5) + ".png"
  image_path =  os.path.join("/tmp", filename)

  plt.savefig(image_path)

  return CorrelationAnalysis(map_filename=filename, strong_corrs=strong_corrs)

def get_agglomerative_clusters(db: Session, file_id: int, contains_headers, columns: list[str], standarization: StandarizationMethod, n_clusters):
  file = get_file_by_id(db, file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not contains_headers else 0)[columns]

  if standarization == StandarizationMethod.NORMALIZER:
    content = __normalize_matrix__(data)
  elif standarization == StandarizationMethod.SCALER:
    content = __scale_matrix__(data)
  else:
    content = data

  clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='complete', metric='euclidean')
  clusters = clustering.fit_predict(content).tolist()

  response = []
  for row in zip(data.to_dict('records'), clusters):
    response.append(
        AgglomerativeClusterResponse(
            id=len(response) + 1,
            properties=row[0],
            cluster=row[1]
        ))
  return response
