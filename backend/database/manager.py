from backend.database.core import SessionLocal, Job
from sqlalchemy import select
from datetime import timedelta


def insert_jobs(jobs):
    with SessionLocal() as db:
        try:
            db.add_all(jobs)
        except Exception:
            ...
            
        db.commit()


def get_jobs_from_date(d):
    
    with SessionLocal() as db:
        statement = select(Job).where((Job.date >= d) & (Job.date < d + timedelta(days=1)))
        results = db.scalars(statement).all()
        return results
    

def unique_jobs_from_date(d):
    with SessionLocal() as db:

        statement = select(Job).where((Job.scrape_date >= d) & (Job.scrape_date < d + timedelta(days=1))).group_by(
            Job.company_name,
            Job.job_title,
            Job.html,
            Job.apply_url,
            Job.publish_date,
            Job.last_apply_date,
            Job.salary,
            Job.location,
            Job.description,
        )
        results = db.scalars(statement).all()
        return results

    