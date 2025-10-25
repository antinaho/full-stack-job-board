from backend.web_scraping.scraper import daily_pipeline
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database.schemas.job import Job
from backend.database.core import Base, engine
from backend.api import register_routes
from backend.app_logging import setup_logging
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from contextlib import asynccontextmanager
global_cache = {'result': None}
@asynccontextmanager
async def lifespan(app: FastAPI):
    daily_pipeline()
    scheduler.start()
    yield
    scheduler.shutdown()
    
#TODO cache the results for a given day. lifespan at the start of the server
# from datetime import datetime
# import pytz
#     today = datetime.now(pytz.timezone('Europe/Helsinki')).date()
#     result = unique_jobs_from_date(today)
#     global_cache['result'] = result
#     yield
#     global_cache['result'] = None

setup_logging()

app = FastAPI(lifespan=lifespan)

scheduler = BackgroundScheduler(timezone=pytz.UTC)
scheduler.add_job(daily_pipeline, "cron", hour=0, minute=0) #3am helsinki time

app.add_middleware(
    CORSMiddleware,
    allow_origins =  ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


Base.metadata.create_all(engine)


register_routes(app)
app.mount("/", StaticFiles(directory="static", html=True, check_dir=False), name="static")