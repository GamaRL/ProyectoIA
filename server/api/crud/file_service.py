import os
import secrets
import shutil
import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session

from ..schemas import FileContent
from ..models import File, FileType

base_path = "/data/files"


def _get_file_path(file: File):
  return os.path.join(base_path, file.file_token) + ".csv"


def save_file(db: Session, file: UploadFile):
  file_token = "file" + secrets.token_urlsafe(5)
  file_name = file.filename.split(".")[0]

  created_file = File(
    name=file_name,
    file_token=file_token,
    algorithm=FileType.APRIORI
  )

  file_path = _get_file_path(created_file)

  with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

  db.add(created_file)
  db.commit()
  db.refresh(created_file)

  return created_file

def delete_file_by_id(db: Session, file_id: int):
  file: File = get_file_by_id(db, file_id)

  file_path = _get_file_path(file)

  db.delete(file)
  os.remove(file_path)

  db.commit()
  return file

def get_files(db: Session, algorithm: FileType):
  return db.query(File).filter(File.algorithm == algorithm).all()

def get_file_by_id(db: Session, file_id: int):
  return db.query(File).filter(File.id == file_id).first()

def get_file_content_by_id(db: Session, file_id: int):
  file: File = get_file_by_id(db, file_id)
  file_path = _get_file_path(file)

  content = pd.read_csv(file_path, header=None)

  head = content.head().stack().groupby(level=0).apply(list).tolist()
  tail = content.tail().stack().groupby(level=0).apply(list).tolist()

  return FileContent(
      head=head,
      tail=tail
  )

def get_file_path_by_id(db: Session, file_id: int):
  file: File = get_file_by_id(db, file_id)
  path: str = _get_file_path(file)

  return path
