from fastapi import APIRouter, status, Request, HTTPException, Depends
from backend.database.core import DbSession
import backend.jobs.service as service
import backend.jobs.models as models
from typing import List
from backend.auth.service import CurrentUser
from backend.auth.service import require_role

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.get("/", response_model=List[models.JobResponse])
def get_jobs(db: DbSession, current_user: CurrentUser, date: str | None = None):
    if date:
        return service.get_jobs_in_date(current_user, db, date)
    return service.get_jobs(current_user, db)


@router.get("/{job_id}", response_model=models.JobResponse)
def get_job(db: DbSession, job_id: int, current_user: CurrentUser):
    return service.get_job_by_id(current_user, db, job_id)


@router.post("/", response_model=models.JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(db: DbSession, job: models.JobCreate, current_user: TokenData = Depends(require_role("admin"))):
    return service.create_job(current_user, db, job)


@router.put("/{job_id}", response_model=models.JobResponse)
def update_job(db: DbSession, job_id: int, job_update: models.JobCreate, current_user: TokenData = Depends(require_role("admin"))):
    return service.update_job(current_user, db, job_id, job_update)

from backend.auth.models import TokenData
@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(db: DbSession, job_id: int, current_user: TokenData = Depends(require_role("admin"))):
    return service.delete_job(current_user, db, job_id)