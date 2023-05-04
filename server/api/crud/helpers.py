import os
import pandas as pd

from sklearn.preprocessing import MinMaxScaler, StandardScaler

from ..models import File


base_path = "/data/files"

def __get_file_path__(file: File):
  return os.path.join(base_path, file.file_token) + ".csv"

def __scale_matrix__(distances: pd.DataFrame):
  scaler = StandardScaler()
  return scaler.fit_transform(distances)

def __normalize_matrix__(distances: pd.DataFrame):
  scaler = MinMaxScaler()
  return scaler.fit_transform(distances)
