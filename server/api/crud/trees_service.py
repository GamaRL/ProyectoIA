import pandas as pd
from sklearn.tree import plot_tree

from sqlalchemy.orm import Session
from sklearn import model_selection
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier

from .file_service import get_file_by_id, __get_file_path__

def train_regression_decision_tree(db: Session, file_id: int):
    file = get_file_by_id(db, file_id)
    path = __get_file_path__(file)
    return None

def get_regression():
    return None

def train_classification_decision_tree(db: Session, file_id: int, max_depth: int, min_samples_split: int, min_samples_leaf: int):
    file = get_file_by_id(db, file_id)
    path = __get_file_path__(file)
    return None

def get_classification():
    return None