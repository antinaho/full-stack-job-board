from fastapi import APIRouter, status, Query, Path
import backend.jobs.service as service
import backend.jobs.models as models
from backend.deps import DbSessionDep
from typing import Annotated
from backend.deps import CurrentAdminUser

router = APIRouter(prefix="/jobs", tags=["Jobs"])

# Year 1900–2099
# Month 01–12
# Day 01-31
date_pattern = "^(?:19|20)\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$"


@router.get("/", response_model=list[models.JobResponse])
def get_jobs(
    db: DbSessionDep,
    date: Annotated[str | None, Query(pattern=date_pattern)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
) -> list[models.JobResponse]:
    return service.get_jobs(db, date, offset, limit)


@router.post(
    "/", response_model=models.JobResponse, status_code=status.HTTP_201_CREATED
)
def create_job(
    db: DbSessionDep, job: models.JobCreate, current_admin: CurrentAdminUser
) -> models.JobResponse:
    return service.create_job(current_admin, db, job)


@router.get("/total_jobs")
def get_total_jobs(
    db: DbSessionDep, date: Annotated[str | None, Query(pattern=date_pattern)] = None
) -> models.JobCount:
    return service.get_total_jobs(db, date)


@router.get("/{job_id}", response_model=models.JobResponse)
def get_job(db: DbSessionDep, job_id: int = Path(..., ge=0)) -> models.JobResponse:
    return service.get_job_by_id(db, job_id)


@router.put("/{job_id}", response_model=models.JobResponse)
def update_job(
    db: DbSessionDep,
    job_id: Annotated[int, Path(..., ge=0)],
    job_update: models.JobCreate,
    current_admin: CurrentAdminUser,
) -> models.JobResponse:
    return service.update_job(current_admin, db, job_id, job_update)


@router.delete(
    "/{job_id}", response_model=models.JobDelete, status_code=status.HTTP_200_OK
)
def delete_job(
    db: DbSessionDep,
    job_id: Annotated[int, Path(..., ge=0)],
    current_admin: CurrentAdminUser,
) -> models.JobDelete:
    return service.delete_job(db, current_admin, job_id)
