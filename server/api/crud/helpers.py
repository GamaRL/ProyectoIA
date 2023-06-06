import os
import pandas as pd

from sklearn.preprocessing import MinMaxScaler, StandardScaler

from ..models import File

base_path = "/data/files"

def __get_file_path__(file: File):
  return os.path.join(base_path, file.file_token) + ".csv"

def __scale_matrix__(distances: pd.DataFrame):
  scaler = StandardScaler()
  return pd.DataFrame(scaler.fit_transform(distances))

def __normalize_matrix__(distances: pd.DataFrame):
  scaler = MinMaxScaler()
  return pd.DataFrame(scaler.fit_transform(distances))

def __validate_numeric_column__(data: pd.DataFrame, col: str):
  return data[col].dtype.kind in 'iufc'

def __validate_numeric_columns__(data: pd.DataFrame):
  for col in data.columns.to_list():
    if data[col].dtype.kind not in 'iufc':
      return False
  return True

def __filter_multiple_columns__(data: pd.DataFrame, n: int = 2):
  cols = []
  for col in data.columns.to_list():
    if data[[col]].nunique().to_list()[0] <= n and data[[col]].nunique().to_list()[0] > 1:
      cols.append(col)
  return cols
