from fastapi import APIRouter, status, Query
import backend.jobs.service as service
import backend.jobs.models as models
from typing import List
from backend.deps import DbSessionDep
from typing import Annotated
from backend.deps import CurrentAdminUser

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# Year 1900–2099
# Month 01–12
# Day 01-31
date_pattern = "^(?:19|20)\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$"


@router.get("/", response_model=List[models.JobResponse])
def get_jobs(
    db: DbSessionDep,
    date: Annotated[str | None, Query(pattern=date_pattern)] = None,
    skip: Annotated[int | None, Query(ge=0)] = 0,
    limit: Annotated[int | None, Query(ge=100)] = 100,
):
    if date:
        return service.get_jobs_in_date(db, date)
    return service.get_jobs(db)


@router.get("/{job_id}", response_model=models.JobResponse)
def get_job(db: DbSessionDep, job_id: Annotated[int, Query(ge=0)]):
    return service.get_job_by_id(db, job_id)


@router.post(
    "/", response_model=models.JobResponse, status_code=status.HTTP_201_CREATED
)
def create_job(
    db: DbSessionDep, job: models.JobCreate, current_admin: CurrentAdminUser
):
    return service.create_job(current_admin, db, job)


@router.put("/{job_id}", response_model=models.JobResponse)
def update_job(
    db: DbSessionDep,
    job_id: int,
    job_update: models.JobCreate,
    current_admin: CurrentAdminUser,
):
    return service.update_job(current_admin, db, job_id, job_update)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(db: DbSessionDep, job_id: int, current_admin: CurrentAdminUser):
    return service.delete_job(db, job_id)
