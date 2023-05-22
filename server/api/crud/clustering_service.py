import os
import secrets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as ptl

from sqlalchemy.orm import Session
from sklearn.cluster import AgglomerativeClustering, KMeans
from kneed import KneeLocator

from ..models import DistanceMetric, StandarizationMethod
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

def get_agglomerative_clusters(db: Session, file_id: int, contains_headers, columns: list[str], standarization: StandarizationMethod, metric: DistanceMetric, no_clusters: int):
  file = get_file_by_id(db, file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not contains_headers else 0)[columns]

  if standarization == StandarizationMethod.NORMALIZER:
    content = __normalize_matrix__(data)
  elif standarization == StandarizationMethod.SCALER:
    content = __scale_matrix__(data)
  else:
    content = data

  if metric == DistanceMetric.EUCLIDEAN:
    clustering = AgglomerativeClustering(n_clusters=no_clusters, linkage='complete', metric='euclidean')
  else:
    clustering = AgglomerativeClustering(n_clusters=no_clusters, linkage='complete', metric='manhattan')

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

def get_agglomerative_cluster_img(db: Session, file_id: int, contains_headers, columns: list[str], standarization: StandarizationMethod, metric: DistanceMetric):
  file = get_file_by_id(db, file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not contains_headers else 0)[columns]

  if standarization == StandarizationMethod.NORMALIZER:
    content = __normalize_matrix__(data)
  elif standarization == StandarizationMethod.SCALER:
    content = __scale_matrix__(data)
  else:
    content = data

  plt.figure(figsize=(15,10))
  ptl.xlabel(file.name)
  ptl.ylabel('Distance')

  if metric == DistanceMetric.EUCLIDEAN:
    shc.dendrogram(shc.linkage(content, method='complete', metric='euclidean'))
  else:
    shc.dendrogram(shc.linkage(content, method='complete', metric='cityblock'))

  ptl.xticks([])
  filename = secrets.token_urlsafe(5) + ".png"
  image_path =  os.path.join("/tmp", filename)

  plt.savefig(image_path)

  return filename

def get_partitional_cluster_img(db: Session, file_id: int, contains_headers, columns: list[str], standarization: StandarizationMethod, metric: DistanceMetric):
  file = get_file_by_id(db, file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not contains_headers else 0)[columns]

  if standarization == StandarizationMethod.NORMALIZER:
    content = __normalize_matrix__(data)
  elif standarization == StandarizationMethod.SCALER:
    content = __scale_matrix__(data)
  else:
    content = data

  sse = []
  for i in range(2, 12):
    km = KMeans(n_clusters=i, random_state=0, n_init='auto')
    km.fit(content)
    sse.append(km.inertia_)

  plt.figure(figsize=(15,10))
  kl = KneeLocator(range(2, 12), sse, curve="convex", direction="decreasing")
  plt.style.use('ggplot')
  kl.plot_knee()

  filename = secrets.token_urlsafe(5) + ".png"
  image_path =  os.path.join("/tmp", filename)

  plt.savefig(image_path)

  return filename

def get_partitional_clusters(db: Session, file_id: int, contains_headers, columns: list[str], standarization: StandarizationMethod, metric: DistanceMetric, no_clusters: int):
  file = get_file_by_id(db, file_id)
  path = __get_file_path__(file)
  data = pd.read_csv(path, header=None if not contains_headers else 0)[columns]

  if standarization == StandarizationMethod.NORMALIZER:
    content = __normalize_matrix__(data)
  elif standarization == StandarizationMethod.SCALER:
    content = __scale_matrix__(data)
  else:
    content = data

  clustering = KMeans(n_clusters=no_clusters, random_state=0, n_init='auto')
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