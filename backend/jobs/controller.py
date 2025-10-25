from fastapi import APIRouter, status, Request, HTTPException
from backend.database.core import DbSession
import backend.jobs.service as service
import backend.jobs.models as models
from typing import List

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.get("/", response_model=List[models.JobResponse])
def get_jobs(db: DbSession, date: str | None = None):
    if date:
        return service.get_jobs_in_date(db, date)
    return service.get_jobs(db)


@router.get("/{job_id}", response_model=models.JobResponse)
def get_job(db: DbSession, job_id: int):
    return service.get_job_by_id(db, job_id)


@router.post("/", response_model=models.JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(request: Request, db: DbSession, job: models.JobCreate):
    client_host = request.client.host
    if client_host not in ("127.0.0.1", "::1"):
        raise HTTPException(status_code=403, detail="Local access only")
    return service.create_job(db, job)


@router.put("/{job_id}", response_model=models.JobResponse)
def update_job(request: Request, db: DbSession, job_id: int, job_update: models.JobCreate):
    client_host = request.client.host
    if client_host not in ("127.0.0.1", "::1"):
        raise HTTPException(status_code=403, detail="Local access only")
    return service.update_job(db, job_id, job_update)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(request: Request, db: DbSession, job_id: int):
    client_host = request.client.host
    if client_host not in ("127.0.0.1", "::1"):
        raise HTTPException(status_code=403, detail="Local access only")
    return service.delete_job(db, job_id)