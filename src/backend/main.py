from src.backend.scrapers.scraper import run_all_scrapers
from src.backend.database.database import insert_jobs

if __name__ == "__main__":
    jobs = run_all_scrapers()
    insert_jobs(jobs)