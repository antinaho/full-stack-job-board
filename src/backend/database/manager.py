from src.backend.database.core import SessionLocal, Job
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
        statement = select(Job).where((Job.scrape_date >= d) & (Job.scrape_date < d + timedelta(days=1)))
        results = db.scalars(statement).all()
        return results

    