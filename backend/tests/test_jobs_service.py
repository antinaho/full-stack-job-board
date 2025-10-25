import pytest
from backend.jobs.models import JobCreate
from backend.jobs import service as jobs_service
from datetime import datetime
import pytz
from backend.exceptions import JobNotFoundError, JobDateNotParsableError
from backend.database.schemas.job import Job

def test_create_job(db_session):
    job_create = JobCreate(
        job_title = "Työntekijä",
        company_name= "Antinaho",
        apply_url = "https://antinaho.com/apply",
        html = "<h1>Hello</h1>"
    )
    
    new_job = jobs_service.create_job(db_session, job_create)
    assert new_job.job_title == "Työntekijä"
    assert new_job.added_on == datetime.now(pytz.timezone("Europe/Helsinki")).date()

def test_get_jobs(db_session, test_job):
    test_job.job_title = "Työntekijä"
    db_session.add(test_job)
    db_session.commit()
    
    jobs = jobs_service.get_jobs(db_session)
    assert len(jobs) == 1
    assert jobs[0].job_title == "Työntekijä"

def test_get_job_by_id(db_session, test_job):
    db_session.add(test_job)
    db_session.commit()
    
    job = jobs_service.get_job_by_id(db_session, test_job.id)
    assert job.id == test_job.id
    
    with pytest.raises(JobNotFoundError):
        jobs_service.get_job_by_id(db_session, 101010)

def test_get_jobs_by_date(db_session, test_job):
    db_session.add(test_job)
    db_session.commit()

    jobs = jobs_service.get_jobs_in_date(db_session, "2001-01-01")
    assert len(jobs) == 1

    with pytest.raises(JobDateNotParsableError):
        jobs_service.get_jobs_in_date(db_session, "Hellurei")


def test_delete_job(db_session, test_job):
    db_session.add(test_job)
    db_session.commit()
    
    jobs_service.delete_job(db_session, test_job.id)
    assert db_session.query(Job).filter_by(id=test_job.id).first() is None 