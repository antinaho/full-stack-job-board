from src.backend.scrapers.scraper import run_all_scrapers

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# api = FastAPI()

# api.add_middleware(
#     CORSMiddleware,
#     allow_origins =  ["https://localhost:4321"],
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"],
# )

# @api.get("/")
# def index():
#     return { "message" : "Hello" }


if __name__ == "__main__":
    jobs = run_all_scrapers()
    # insert_jobs(jobs)
    # transform_jobs()
    