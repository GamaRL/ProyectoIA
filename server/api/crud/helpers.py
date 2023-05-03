import pandas as pd

from sklearn.preprocessing import MinMaxScaler, StandardScaler

def __scale_matrix__(distances: pd.DataFrame):
  scaler = StandardScaler()
  return scaler.fit_transform(distances)

def __normalize_matrix__(distances: pd.DataFrame):
  scaler = MinMaxScaler()
  return scaler.fit_transform(distances)
