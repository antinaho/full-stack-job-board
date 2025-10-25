from bs4 import element
from datetime import datetime
import re
import pytz

from backend.database.schemas.job import Job

parsers = {}

def parse_kesko(company_name: str, raw_html: element.Tag) -> Job:
    
    try: #Job title
        title = raw_html.select_one("a.head3").text
    except Exception:
        title = None

    # try: # Last apply date
    #     last_apply_date_element = raw_html.select_one("p.pull-right-sm > span").next_sibling().strip()
    #     match = re.search(r'\d{2}\.\d{2}\.\d{4}', last_apply_date_element)
    #     last_apply_date = match.group()
    #     last_apply_date = datetime.strptime(last_apply_date, '%d.%m.%Y')
    # except Exception:
    #     last_apply_date = None

    # try: # Publish date
    #     publish_date_element = raw_html.select_one("div.col-sm-10.col-xs-12").contents[0].strip()
    #     match = re.search(r'\d{1,2}\.\d{1,2}\.\d{4}', publish_date_element)
    #     publish_date = match.group()
    #     publish_date = datetime.strptime(publish_date, '%d.%m.%Y')
    # except Exception:
    #     publish_date = None

    try: # Apply url
        apply_url = raw_html.select_one("a.head3").get("href")
    except Exception:
        apply_url = None

    return Job(
        company_name = company_name,
        job_title = str(title),
        added_on = datetime.now(pytz.timezone('Europe/Helsinki')).date(),
        html = str(raw_html),
        apply_url = str(apply_url),
    )
parsers["parse_kesko"] = parse_kesko


def parse_supercell(company_name: str, raw_html: element.Tag) -> Job:

    try: #Job title
        title = raw_html.select_one("div.Offers_title__y_jGJ").text
    except Exception:
        title = None

    try: # Apply url
        url_head = "https://supercell.com"
        apply_url = raw_html.select_one("a").get("href")
        apply_url = url_head + apply_url
    except Exception:
        apply_url = None

    try: # Location
        location = raw_html.select_one("div.Offers_location__5xwTM").contents[0]
    except Exception:
        location = None

    if location == None or str(location) != "Helsinki":
        return None
 
    return Job(
        company_name = company_name,
        job_title = str(title),
        added_on = datetime.now(pytz.timezone('Europe/Helsinki')).date(),
        html = str(raw_html),
        apply_url = str(apply_url),
    )
parsers["parse_supercell"] = parse_supercell
