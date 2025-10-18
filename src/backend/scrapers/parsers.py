from bs4 import element
from datetime import datetime

from src.backend.database.core import Job

parsers = {}

# Kesko
def parse_kesko(company_name: str, raw_html: element.Tag) -> Job:
    title = raw_html.select_one("a.head3").text

    return Job(
        company_name = company_name,
        job_title = title,
        scrape_date = datetime.now(),
        html = raw_html,
        apply_url = None,
        salary = None,
        location = None,
        description = None
    )

parsers["parse_kesko"] = parse_kesko