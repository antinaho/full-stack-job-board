from src.backend.web_scraping.scraper import run_all_scrapers
from src.backend.database.manager import insert_jobs, get_jobs_from_date, unique_jobs_from_date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
from threading import Lock
from contextlib import asynccontextmanager


cache_lock = Lock()
global_cache = {'result': None}

@asynccontextmanager
async def lifespan(app: FastAPI):
    today = datetime.now(pytz.timezone('Europe/Helsinki')).date()
    result = unique_jobs_from_date(today)
    global_cache['result'] = result
    yield
    global_cache['result'] = None

api = FastAPI(lifespan=lifespan)

api.add_middleware(
    CORSMiddleware,
    allow_origins =  ["https://localhost:4321"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@api.get("/")
def index():
    return global_cache['result']

def daily_pipeline():
    jobs = run_all_scrapers()
    insert_jobs(jobs)