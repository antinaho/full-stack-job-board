from bs4 import element
from datetime import datetime
import re
import pytz

from src.backend.database.core import Job

parsers = {}

# Kesko
def parse_kesko(company_name: str, raw_html: element.Tag) -> Job:
    
    try: #Job title
        title = raw_html.select_one("a.head3").text
    except Exception:
        title = None

    try: # Last apply date
        last_apply_date_element = raw_html.select_one("p.pull-right-sm > span").next_sibling().strip()
        match = re.search(r'\d{2}\.\d{2}\.\d{4}', last_apply_date_element)
        last_apply_date = match.group()
        last_apply_date = datetime.strptime(last_apply_date, '%d.%m.%Y')
    except Exception:
        last_apply_date = None

    try: # Publish date
        publish_date_element = raw_html.select_one("div.col-sm-10.col-xs-12").contents[0].strip()
        match = re.search(r'\d{1,2}\.\d{1,2}\.\d{4}', publish_date_element)
        publish_date = match.group()
        publish_date = datetime.strptime(publish_date, '%d.%m.%Y')
    except Exception:
        publish_date = None

    try: # Apply url
        apply_url = raw_html.select_one("a.head3").get("href")
    except Exception:
        apply_url = None

    return Job(
        company_name = company_name,
        job_title = str(title),
        scrape_date = datetime.now(pytz.timezone('Europe/Helsinki')),
        html = str(raw_html),
        publish_date = publish_date,
        last_apply_date = last_apply_date,
        apply_url = str(apply_url),
        salary = None,
        location = None,
        description = None
    )

parsers["parse_kesko"] = parse_kesko