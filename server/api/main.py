from typing import List
from fastapi import Depends, FastAPI, File, Request, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import models
from .schemas import AssociationRuleRow
from .crud.file_service import _get_file_path, delete_file_by_id, get_file_by_id, get_file_content_by_id, get_files, save_file
from .crud.apriori_service import get_frequency_table_from_file, get_rule_from_file, get_rules_from_file, save_rule_from_file

from .database import Base, SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency


def get_db(request: Request):
    return request.state.db


# Association rules endpoints


@app.post("/1/files/")
async def api_create_file(db: Session = Depends(get_db), file: UploadFile = File(...)):
    return save_file(db, file)


@app.get("/1/files/")
async def api_get_files(db: Session = Depends(get_db)):
    return get_files(db, models.FileType.APRIORI)


@app.delete("/1/files/{file_id}")
async def api_delete_file(file_id: int, db: Session = Depends(get_db)):
    return delete_file_by_id(db, file_id)


@app.get("/1/files/{file_id}")
async def api_get_file(file_id: int, download: bool = False, db: Session = Depends(get_db)):
    if download:
        file: models.File = get_file_by_id(db, file_id)
        path: str = _get_file_path(file)
        return FileResponse(path, filename=file.name, media_type="text/csv")

    return get_file_content_by_id(db, file_id)


@app.get("/1/statistics/{file_id}")
async def api_get_statistics(file_id: int, db: Session = Depends(get_db)):
    return get_frequency_table_from_file(db, file_id)

@app.get("/1/rules/{file_id}")
async def api_get_rules(
    file_id: int,
    min_support: float,
    min_confidence: float,
    min_lift: float,
    db: Session = Depends(get_db)):
    return get_rules_from_file(db, file_id, min_support, min_confidence, min_lift)

@app.post("/1/rules/{file_id}")
async def api_get_rules(
    file_id: int,
    rules: list[AssociationRuleRow],
    db: Session = Depends(get_db)):
    return save_rule_from_file(db, file_id, rules)

@app.get("/1/rules/{file_id}/all")
async def api_get_rules_all(
    file_id: int,
    db: Session = Depends(get_db)):
    return get_rule_from_file(db, file_id)
