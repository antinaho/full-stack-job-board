from bs4 import element
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Job:
    company_name: str
    scrape_time_stamp: str
    job_title: str
    raw_html: str


parsers = {}


def datetime_now_iso(): return datetime.now().isoformat()

# Kesko
def parse_kesko(company_name: str, raw_html: element.Tag) -> Job:
    title = raw_html.select_one("a.head3").text

    return Job(
        company_name=company_name,
        scrape_time_stamp=datetime_now_iso(),
        job_title=str(title),
        raw_html=str(raw_html)
    )

parsers["parse_kesko"] = parse_kesko