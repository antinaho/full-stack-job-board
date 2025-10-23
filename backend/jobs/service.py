from sqlalchemy.orm import Session
from backend.database.schemas.job import Job
import backend.jobs.models as models
from datetime import datetime
import pytz
from backend.exceptions import JobNotFoundError
from fastapi import HTTPException

def get_jobs(db: Session) -> list[models.JobResponse]:
    jobs = db.query(Job).all()
    return jobs


def get_jobs_in_date(db: Session, date_string: str) -> list[models.JobResponse]:
    try:
        queried_date = datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    jobs = (
        db.query(Job.company_name, Job.job_title, Job.apply_url)
        .filter(Job.added_on == queried_date)
        .distinct(Job.company_name, Job.job_title, Job.apply_url)
        .all()
    )
    return jobs


def get_job_by_id(db: Session, job_id: int) -> Job:
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise JobNotFoundError(job_id)
    return job


# def create_job(db: Session, job: models.JobCreate) -> Job:
#     try:
#         new_job = Job(**job.model_dump())

#         new_job.added_on = datetime.now(pytz.timezone('Europe/Helsinki')).date()

#         db.add(new_job)
#         db.commit()
#         db.refresh(new_job)
#         return new_job
#     except Exception as e:
#         raise JobCreationError(str(e))