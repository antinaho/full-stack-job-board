from backend.web_scraping.scraper import daily_pipeline
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database.core import Base, engine
from backend.api import register_routes
from backend.app_logging import setup_logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from contextlib import asynccontextmanager
from backend.auth.service import register_super_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_super_user()
    daily_pipeline()
    scheduler.start()
    yield
    scheduler.shutdown()


setup_logging()

app = FastAPI(lifespan=lifespan)

scheduler = BackgroundScheduler(timezone=pytz.timezone("Europe/Helsinki"))
trigger = CronTrigger(hour=1, minute=0, timezone=pytz.timezone("Europe/Helsinki"))
scheduler.add_job(daily_pipeline, trigger)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)

register_routes(app)
app.mount(
    "/",
    StaticFiles(directory="backend/static", html=True, check_dir=False),
    name="static",
)
