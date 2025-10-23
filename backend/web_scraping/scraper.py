import os
import json
import requests as r
from bs4 import BeautifulSoup
from backend.web_scraping.parser import parsers
from backend.database.core import SessionLocal


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config():
    with open(os.path.join(BASE_DIR, "config/sites.json"), "r") as f:
        sites = json.load(f)

    return sites


def scrape_html(site):
    response = r.get(site["url"])
    soup = BeautifulSoup(response.text, "lxml")

    job_elements = soup.select(site["single_job_selector"])
    
    normalized_name = site["name"].lower().replace(" ", "_")
    func_name = f"parse_{normalized_name}"
    parser_func = parsers.get(func_name)
    
    if not parser_func or not callable(parser_func):
        raise ValueError(f"No parser function found for site: {site["name"]}, expected function: {func_name}")

    jobs = []
    for job_element in job_elements:
        
        job = parser_func(site["name"], job_element)
        if job == None:
            continue
        jobs.append(job)
    
    return jobs


def run_all_scrapers():
    sites = load_config()
    all_jobs = []
    for site in sites:

        scraper_type = site["scraper_type"]
        
        if scraper_type == "html":
            jobs = scrape_html(site)
        elif scraper_type == "api":
            ...

        all_jobs.extend(jobs)

    return all_jobs


def add_to_db(jobs):
    db = SessionLocal()
    for job in jobs:
        try:
            db.add(job)
            db.commit()
            db.refresh(job)
        except:
            db.rollback()
    db.close()


def daily_pipeline():
    jobs = run_all_scrapers()
    add_to_db(jobs)


if __name__ == "__main__":
    daily_pipeline()