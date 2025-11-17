import pytest
from backend.jobs.models import JobCreate
from backend.jobs import service as jobs_service
from backend.exceptions import JobNotFoundError, JobDateNotParsableError
from backend.database.schemas.job import Job
from backend.auth.models import TokenData
from backend.database.schemas.user import UserRole


def test_create_job(db_session):
    job_create = JobCreate(
        job_title="Työntekijä",
        company_name="Antinaho",
        apply_url="https://antinaho.com/apply",
        html="<h1>Hello</h1>",
    )

    token_data = TokenData(user_id="123", user_role=str(UserRole.USER))

    new_job = jobs_service.create_job(token_data, db_session, job_create)
    assert new_job.job_title == "Työntekijä"


def test_get_jobs(db_session, test_job):
    test_job.job_title = "Työntekijä"
    db_session.add(test_job)
    db_session.commit()

    from datetime import datetime

    date_string = datetime.strftime(test_job.added_on, "%Y-%m-%d")

    jobs = jobs_service.get_jobs(db_session, date_string, 0, 10)
    assert len(jobs) == 1
    assert jobs[0].job_title == "Työntekijä"


def test_get_job_by_id(db_session, test_job):
    db_session.add(test_job)
    db_session.commit()

    job = jobs_service.get_job_by_id(db_session, test_job.id)
    assert job.apply_url == test_job.apply_url
    assert job.company_name == test_job.company_name

    with pytest.raises(JobNotFoundError):
        jobs_service.get_job_by_id(db_session, 101010)


def test_get_jobs_by_date(db_session, test_job):
    db_session.add(test_job)
    db_session.commit()

    jobs = jobs_service.get_jobs(db_session, "2001-01-01", 0, 10)
    assert len(jobs) == 1

    with pytest.raises(JobDateNotParsableError):
        jobs_service.get_jobs(db_session, "Hellurei", 0, 10)


def test_delete_job(db_session, test_job):
    db_session.add(test_job)
    db_session.commit()

    token_data = TokenData(user_id="123", user_role=str(UserRole.ADMIN))

    jobs_service.delete_job(db_session, token_data, test_job.id)
    assert db_session.query(Job).filter_by(id=test_job.id).first() is None
