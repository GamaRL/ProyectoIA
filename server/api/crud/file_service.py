import os
import secrets
import shutil
import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session

from ..schemas import FileContent
from ..models import File, FileType, StandarizationMethod
from .helpers import __get_file_path__ ,__scale_matrix__, __normalize_matrix__


def save_file(db: Session, file: UploadFile, type: FileType):
  file_token = "file" + secrets.token_urlsafe(5)
  file_name = file.filename.split(".")[0]

  created_file = File(
    name=file_name,
    file_token=file_token,
    algorithm=type
  )

  file_path = __get_file_path__(created_file)

  with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

  db.add(created_file)
  db.commit()
  db.refresh(created_file)

  return created_file

def delete_file_by_id(db: Session, file_id: int):
  file: File = get_file_by_id(db, file_id)

  file_path = __get_file_path__(file)

  db.delete(file)
  os.remove(file_path)

  db.commit()
  return file

def get_files(db: Session, algorithm: FileType):
  return db.query(File).filter(File.algorithm == algorithm).all()

def get_file_by_id(db: Session, file_id: int):
  return db.query(File).filter(File.id == file_id).first()

def get_file_content_with_headers_by_id(db: Session, file_id: int, contains_headers: bool, columns: list[str], method: StandarizationMethod):
  file: File = get_file_by_id(db, file_id)
  file_path = __get_file_path__(file)

  content = pd.read_csv(file_path, header=None if not contains_headers else 0)

  content = content[columns]

  if method == StandarizationMethod.NORMALIZER:
    content = __normalize_matrix__(content)
    content = pd.DataFrame(content).round(2)
  elif method == StandarizationMethod.SCALER:
    content = __scale_matrix__(content)
    content = pd.DataFrame(content).round(4)

  headers = content.columns.to_list()
  head = content.head().stack().groupby(level=0).apply(list).tolist()
  tail = content.tail().stack().groupby(level=0).apply(list).tolist()

  return FileContent(
      headers=headers,
      head=head,
      tail=tail
  )

def get_file_content_by_id(db: Session, file_id: int):
  file: File = get_file_by_id(db, file_id)
  file_path = __get_file_path__(file)

  content = pd.read_csv(file_path, header=None)

  head = content.head().stack().groupby(level=0).apply(list).tolist()
  tail = content.tail().stack().groupby(level=0).apply(list).tolist()

  return FileContent(
      head=head,
      tail=tail
  )

def get_file_path_by_id(db: Session, file_id: int):
  file: File = get_file_by_id(db, file_id)
  path: str = __get_file_path__(file)

  return path

def get_file_headers(db: Session, file_id: int, contains_header: bool):
  file: File = get_file_by_id(db, file_id)
  file_path = __get_file_path__(file)
  content = pd.read_csv(file_path, header=None if not contains_header else 0)

  return content.columns.to_list()