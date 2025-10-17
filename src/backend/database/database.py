from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, insert

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
metadata_obj = MetaData()

job_table = Table(
    "jobs",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("company_name", String),
    Column("job_title", String),
    Column("scrape_time_stamp", String),
    Column("raw_html", String)
)

metadata_obj.create_all(engine)

def insert_jobs(jobs):
    with engine.begin() as conn:

        conn.execute(
            insert(job_table),
            jobs
        )