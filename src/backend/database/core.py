from sqlalchemy import create_engine, DateTime, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
from fastapi import Depends
from typing import Annotated

DATABASE_URL = "sqlite+pysqlite:///database.db" 
#DATABASE_URL = "sqlite+pysqlite:///:memory:" 

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    scrape_date = Column(DateTime, nullable=False)
    html = Column(String, nullable=False)
    apply_url = Column(String, nullable=True)

    publish_date = Column(DateTime, nullable=True)
    last_apply_date = Column(DateTime, nullable=True)
    salary = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(String, nullable=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"

    def __repr__(self):
        return (f"Job(id={self.id}, company_name='{self.company_name}', "
                f"job_title='{self.job_title}', scrape_date={self.scrape_date}, "
                f"apply_url='{self.apply_url}', publish_date={self.publish_date}, "
                f"last_apply_date={self.last_apply_date}, salary='{self.salary}', "
                f"location='{self.location}')")


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

DbSession = Annotated[Session, Depends(get_db)]
