from fastapi import APIRouter, status
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


# @router.post("/", response_model=models.JobResponse, status_code=status.HTTP_201_CREATED)
# def create_job(db: DbSession, job: models.JobCreate):
#     return service.create_job(db, job)