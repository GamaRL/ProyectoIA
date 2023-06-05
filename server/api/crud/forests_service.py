import pandas as pd

from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestRegressor

from .file_service import get_file_by_id, __get_file_path__