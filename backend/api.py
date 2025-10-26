from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.jobs.controller import router as jobs_router


def register_routes(app: FastAPI):
    app.include_router(jobs_router)
    
