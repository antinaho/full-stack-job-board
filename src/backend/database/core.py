from sqlalchemy import create_engine, MetaData, DateTime, Table, Column, Integer, String, insert, select
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime

DATABASE_URL = "sqlite+pysqlite:///:memory:" 

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    scrape_date = Column(DateTime, nullable=False)
    html = Column(String, nullable=False)
    apply_url = Column(String, nullable=True)

    salary = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<Job({self.company_name=}, {self.job_title=})"


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()