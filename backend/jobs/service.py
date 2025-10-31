from sqlalchemy.orm import Session
from backend.database.schemas.job import Job
import backend.jobs.models as models
from datetime import datetime
import pytz
from backend.exceptions import (
    JobNotFoundError,
    JobCreationError,
    JobDateNotParsableError,
)
import logging
import backend.jobs.caching as jc
import backend.auth.models as auth_models


def get_jobs(db: Session) -> list[models.JobResponse]:
    jobs = db.query(Job).all()
    logging.info(f"Retrieved {len(jobs)} jobs.")
    return jobs


def get_jobs_in_date(db: Session, date_string: str) -> list[models.JobResponse]:
    try:
        queried_date = datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError as e:
        logging.error(
            f"Tried passing invalid date string {date_string}. Error: {str(e)}"
        )
        raise JobDateNotParsableError(str(e))

    if queried_date == jc.job_cache[0]:
        jobs = jc.job_cache[1]
        logging.info(
            f"Retrieved {len(jobs)} unique jobs for date {queried_date} from cache"
        )
        return jobs

    now_date = datetime.now().date()
    if queried_date > now_date:
        logging.warning("Trying to look up jobs in the future")
        return []

    jobs = (
        db.query(Job.company_name, Job.job_title, Job.apply_url)
        .filter(Job.added_on == queried_date)
        .distinct(Job.company_name, Job.job_title, Job.apply_url)
        .all()
    )

    logging.info(f"Retrieved {len(jobs)} unique jobs for date {queried_date}")
    return jobs


def get_job_by_id(db: Session, job_id: int) -> Job:
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        logging.error(f"Job not found with id {job_id}")
        raise JobNotFoundError(job_id)
    logging.info(f"Retrieved job {job_id}")
    return job


def create_job(
    current_user: auth_models.TokenData, db: Session, job: models.JobCreate
) -> Job:
    try:
        new_job = Job(**job.model_dump())

        new_job.added_on = datetime.now(pytz.timezone("Europe/Helsinki")).date()

        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        logging.info("New job created")
        return new_job
    except Exception as e:
        logging.error(f"Job creation error: {str(e)}")
        raise JobCreationError(str(e))


def update_job(
    current_user: auth_models.TokenData,
    db: Session,
    job_id: int,
    job_update: models.JobCreate,
) -> Job:
    job_data = job_update.model_dump(exclude_unset=True)
    db.query(Job).filter(Job.id == job_id).update(job_data)
    db.commit()
    logging.info(f"Successfully updated job {job_id}")
    return get_job_by_id(db, job_id)


def delete_job(db: Session, job_id: int) -> None:
    job = get_job_by_id(db, job_id)
    db.delete(job)
    db.commit()
    logging.info(f"Job {job_id} deleted")
