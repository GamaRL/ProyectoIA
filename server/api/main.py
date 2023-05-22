import os
from typing import Annotated
from fastapi import Depends, FastAPI, File, Query, Request, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import models
from .schemas import AssociationRuleRow
from .crud.file_service import __get_file_path__, delete_file_by_id, get_file_by_id, get_file_content_by_id, get_file_content_with_headers_by_id, get_file_headers, get_files, save_file
from .crud.apriori_service import get_frequency_table_from_file, get_rule_from_file, get_rules_from_file, save_rule_from_file
from .crud.distances_service import get_distances_from_file_by_id
from .crud.clustering_service import get_agglomerative_cluster_img, get_agglomerative_clusters, get_correlation_matrix, get_partitional_cluster_img, get_partitional_clusters

from .database import SessionLocal, engine


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

@app.post("/0/files/")
async def api_create_file(db: Session = Depends(get_db), file: UploadFile = File(...)):
    return save_file(db, file, models.FileType.APRIORI)


@app.get("/0/files/")
async def api_get_files(db: Session = Depends(get_db)):
    return get_files(db, models.FileType.APRIORI)


@app.delete("/0/files/{file_id}")
async def api_delete_file(file_id: int, db: Session = Depends(get_db)):
    return delete_file_by_id(db, file_id)


@app.get("/0/files/{file_id}")
async def api_get_file(file_id: int, download: bool = False, db: Session = Depends(get_db)):
    if download:
        file: models.File = get_file_by_id(db, file_id)
        path: str = __get_file_path__(file)
        return FileResponse(path, filename=file.name, media_type="text/csv")

    return get_file_content_by_id(db, file_id)

@app.get("/0/statistics/{file_id}")
async def api_get_statistics(file_id: int, db: Session = Depends(get_db)):
    return get_frequency_table_from_file(db, file_id)

@app.get("/0/rules/{file_id}")
async def api_get_rules(
    file_id: int,
    min_support: float,
    min_confidence: float,
    min_lift: float,
    db: Session = Depends(get_db)):
    return get_rules_from_file(db, file_id, min_support, min_confidence, min_lift)

@app.post("/0/rules/{file_id}")
async def api_get_rules(
    file_id: int,
    rules: list[AssociationRuleRow],
    db: Session = Depends(get_db)):
    return save_rule_from_file(db, file_id, rules)

@app.get("/0/rules/{file_id}/all")
async def api_get_rules_all(
    file_id: int,
    db: Session = Depends(get_db)):
    return get_rule_from_file(db, file_id)


# Distances endpoints

@app.post("/1/files/")
async def dist_api_create_file(db: Session = Depends(get_db), file: UploadFile = File(...)):
    return save_file(db, file, models.FileType.DISTANCES)

@app.get("/1/files/")
async def dist_api_get_files(db: Session = Depends(get_db)):
    return get_files(db, models.FileType.DISTANCES)

@app.delete("/1/files/{file_id}")
async def dist_api_delete_file(file_id: int, db: Session = Depends(get_db)):
    return delete_file_by_id(db, file_id)

@app.get("/1/files/{file_id}")
async def dist_api_get_file(file_id: int, download: bool = False, db: Session = Depends(get_db)):
    if download:
        file: models.File = get_file_by_id(db, file_id)
        path: str = __get_file_path__(file)
        return FileResponse(path, filename=file.name, media_type="text/csv")

    return get_file_content_by_id(db, file_id)

@app.get("/1/files/{file_id}/headers")
async def dist_api_get_headers(file_id: int, contains_headers: bool = False, db: Session = Depends(get_db)):
    return get_file_headers(db, file_id, contains_headers)

@app.get("/1/files/{file_id}/content")
async def dist_api_get_file_with_headers(file_id: int, contains_headers: bool = False, columns: Annotated[list[str], Query()] = [], method: Annotated[models.StandarizationMethod, Query()] = models.StandarizationMethod.NONE, db: Session = Depends(get_db)):
    if not contains_headers:
        columns = list(map(lambda p: int(p), columns))
    return get_file_content_with_headers_by_id(db, file_id, contains_headers, columns, method)

@app.get("/1/files/{file_id}/distances")
async def dist_api_get_file_distances(
    file_id: int,
    download: bool = False,
    contains_headers: bool = False,
    columns: Annotated[list[str], Query()] = [],
    metric: Annotated[models.DistanceMetric, Query()] = models.DistanceMetric.EUCLIDEAN,
    standarization: Annotated[models.StandarizationMethod, Query()] = models.StandarizationMethod.NONE,
    db: Session = Depends(get_db)):

    response = get_distances_from_file_by_id(db, file_id, download, contains_headers, columns, metric, standarization)

    if download:
        return FileResponse(response, media_type="text/csv")
    return response

# Clustering endpoints

@app.post("/2/files/")
async def clust_api_create_file(db: Session = Depends(get_db), file: UploadFile = File(...)):
    return save_file(db, file, models.FileType.CLUSTERING)

@app.get("/2/files/")
async def clust_api_get_files(db: Session = Depends(get_db)):
    return get_files(db, models.FileType.CLUSTERING)

@app.delete("/2/files/{file_id}")
async def clust_api_delete_file(file_id: int, db: Session = Depends(get_db)):
    return delete_file_by_id(db, file_id)

@app.get("/2/files/{file_id}")
async def clust_api_get_file(file_id: int, download: bool = False, db: Session = Depends(get_db)):
    if download:
        file: models.File = get_file_by_id(db, file_id)
        path: str = __get_file_path__(file)
        return FileResponse(path, filename=file.name, media_type="text/csv")

    return get_file_content_by_id(db, file_id)

@app.get("/2/files/{file_id}/headers")
async def clust_api_get_headers(file_id: int, contains_headers: bool = False, db: Session = Depends(get_db)):
    return get_file_headers(db, file_id, contains_headers)

@app.get("/2/files/{file_id}/dimensionality")
async def clust_api_get_dimensionality(
    file_id: int,
    contains_headers: bool = False,
    standarization: Annotated[models.StandarizationMethod, Query()] = models.StandarizationMethod.NONE,
    db: Session = Depends(get_db)):

    return get_correlation_matrix(db, file_id, contains_headers, standarization)

@app.get("/2/images/{filename}")
async def clust_api_get_map(
    filename: str,
    db: Session = Depends(get_db)):
        path = os.path.join("/tmp", filename)
        return FileResponse(path, filename=filename, media_type="img/png")

@app.get("/2/files/{file_id}/agglomerative")
async def clust_api_get_agglomerative(
    file_id: int,
    contains_headers: bool = False,
    columns: Annotated[list[str], Query()] = [],
    standarization: Annotated[models.StandarizationMethod, Query()] = models.StandarizationMethod.NONE,
    metric: Annotated[models.DistanceMetric, Query()] = models.DistanceMetric.EUCLIDEAN,
    no_clusters: int = 7,
    db: Session = Depends(get_db)):
    return get_agglomerative_clusters(db, file_id, contains_headers, columns, standarization, metric, no_clusters)

@app.get("/2/files/{file_id}/agglomerative/img")
async def clust_api_get_agglomerative_img(
    file_id: int,
    contains_headers: bool = False,
    columns: Annotated[list[str], Query()] = [],
    standarization: Annotated[models.StandarizationMethod, Query()] = models.StandarizationMethod.NONE,
    metric: Annotated[models.DistanceMetric, Query()] = models.DistanceMetric.EUCLIDEAN,
    db: Session = Depends(get_db)):
    return get_agglomerative_cluster_img(db, file_id, contains_headers, columns, standarization, metric)

@app.get("/2/files/{file_id}/partitional/img")
async def clust_api_get_agglomerative_img(
    file_id: int,
    contains_headers: bool = False,
    columns: Annotated[list[str], Query()] = [],
    standarization: Annotated[models.StandarizationMethod, Query()] = models.StandarizationMethod.NONE,
    metric: Annotated[models.DistanceMetric, Query()] = models.DistanceMetric.EUCLIDEAN,
    db: Session = Depends(get_db)):
    return get_partitional_cluster_img(db, file_id, contains_headers, columns, standarization, metric)

@app.get("/2/files/{file_id}/partitional")
async def clust_api_get_agglomerative(
    file_id: int,
    contains_headers: bool = False,
    columns: Annotated[list[str], Query()] = [],
    standarization: Annotated[models.StandarizationMethod, Query()] = models.StandarizationMethod.NONE,
    metric: Annotated[models.DistanceMetric, Query()] = models.DistanceMetric.EUCLIDEAN,
    no_clusters: int = 7,
    db: Session = Depends(get_db)):
    return get_partitional_clusters(db, file_id, contains_headers, columns, standarization, metric, no_clusters)