from src.backend.web_scraping.scraper import run_all_scrapers
from src.backend.database.manager import insert_jobs, get_jobs_from_date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
from contextlib import asynccontextmanager

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins =  ["https://localhost:4321"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@api.get("/")
def index():
    today = datetime.now(pytz.timezone('Europe/Helsinki')).date()
    return get_jobs_from_date(today)


def daily_pipeline():
    jobs = run_all_scrapers()
    insert_jobs(jobs)

if __name__ == "__main__":
    pass
    