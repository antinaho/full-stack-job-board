from backend.web_scraping.scraper import run_all_scrapers
from backend.database.manager import insert_jobs, get_jobs_from_date, unique_jobs_from_date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz
from threading import Lock
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles


cache_lock = Lock()
global_cache = {'result': None}

def daily_pipeline():
    jobs = run_all_scrapers()
    insert_jobs(jobs)

@asynccontextmanager
async def lifespan(app: FastAPI):
    daily_pipeline()
    today = datetime.now(pytz.timezone('Europe/Helsinki')).date()
    result = unique_jobs_from_date(today)
    global_cache['result'] = result
    yield
    global_cache['result'] = None
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins =  ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/api/unique_jobs/")
def index():
    return global_cache['result']

app.mount("/", StaticFiles(directory="static", html=True, check_dir=False), name="static")

if __name__ == "__main__":
    daily_pipeline()
    today = datetime.now(pytz.timezone('Europe/Helsinki')).date()
    result = unique_jobs_from_date(today)
    global_cache['result'] = result