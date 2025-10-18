from src.backend.database.core import SessionLocal
from sqlalchemy import insert

def insert_jobs(jobs):
    with SessionLocal() as db:
        for job in jobs:
            try:
                db.add(job)
                db.flush()
            except Exception:
                ...
        db.commit()