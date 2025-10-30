from fastapi import FastAPI

from backend.jobs.controller import router as jobs_router
from backend.auth.controller import router as auth_router

def register_routes(app: FastAPI):
    app.include_router(jobs_router)
    app.include_router(auth_router)
