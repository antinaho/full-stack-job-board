from datetime import datetime, date, timedelta

job_cache = {}

def clear_expired_jobs():

    date_now = datetime.now()
    oldest_entry_date = (date_now - timedelta(days=3)).date()

    for k, v in job_cache.items():
        if k <= oldest_entry_date:
            del job_cache[k]
