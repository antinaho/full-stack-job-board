from sqlalchemy.orm import Session
from sqlalchemy import select, update
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
import backend.auth.models as auth_models


def get_jobs(
    db: Session, date_string: str | None, skip: int, limit: int
) -> list[models.JobResponse]:
    stmt = select(Job).distinct(Job.company_name, Job.job_title, Job.apply_url)

    if date_string is not None:
        # date_string should be in valid format from previous url validation before this function was called, no need to try/except
        date = datetime.strptime(date_string, "%Y-%m-%d").date()
        stmt = stmt.where(Job.added_on == date)

    stmt = stmt.offset(skip).limit(limit)

    result = db.execute(stmt)
    jobs = result.scalars().all()

    jobs_response = [models.JobResponse.model_validate(job) for job in jobs]

    logging.info(f"Retrieved {len(jobs_response)} jobs.")

    return jobs_response


def get_total_jobs(db: Session, date_string: str | None) -> models.JobCount:
    stmt = select(Job).distinct(Job.company_name, Job.job_title, Job.apply_url)

    if date_string is not None:
        # date_string should be in valid format from previous url validation before this function was called, no need to try/except
        date = datetime.strptime(date_string, "%Y-%m-%d").date()
        stmt = stmt.where(Job.added_on == date)

    result = db.execute(stmt)
    jobs = result.scalars().all()

    logging.info("Retrieved job count.")

    return models.JobCount(count=len(jobs))


def get_job_by_id(db: Session, job_id: int) -> models.JobResponse:
    stmt = select(Job).where(Job.id == job_id)
    job = db.execute(stmt).scalar()
    if job is None:
        logging.error(f"Job not found with id {job_id}")
        raise JobNotFoundError(job_id)

    logging.info(f"Retrieved job {job_id}")

    return models.JobResponse.model_validate(job)


def create_job(
    current_user: auth_models.TokenData, db: Session, job: models.JobCreate
) -> models.JobResponse:
    try:
        new_job: Job = Job(**job.model_dump())

        new_job.added_on = datetime.now(pytz.timezone("Europe/Helsinki")).date()  # type: ignore

        db.add(new_job)
        db.commit()
        db.refresh(new_job)

        logging.info(f"New job created by {current_user.user_id}")
        return models.JobResponse.model_validate(new_job)
    except Exception as e:
        logging.error(f"Job creation error: {str(e)}")
        raise JobCreationError(str(e))


def update_job(
    current_user: auth_models.TokenData,
    db: Session,
    job_id: int,
    job_update: models.JobCreate,
) -> models.JobResponse:
    job_data = job_update.model_dump(exclude_unset=True)

    stmt = (
        update(Job)
        .where(Job.id == job_id)
        .values(**job_data)
        .execution_options(synchronize_session="fetch")
    )

    db.execute(stmt)
    db.commit()

    logging.info(f"Successfully updated job {job_id}. By {current_user.user_id}")
    return get_job_by_id(db, job_id)


def delete_job(
    db: Session, current_admin: auth_models.TokenData, job_id: int
) -> models.JobDelete:
    result = db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if job is None:
        logging.error(f"Job not found with id {job_id}")
        raise JobNotFoundError(job_id)

    db.delete(job)
    db.commit()

    logging.info(f"Job {job_id} deleted")
    return models.JobDelete(id=job_id)
