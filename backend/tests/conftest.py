import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.core import Base
from backend.database.schemas.job import Job
from datetime import datetime


@pytest.fixture(scope="function")
def db_session():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_job():
    return Job(
        id = 100,
        company_name = "Antinaho",
        job_title = "Chiller",
        added_on = datetime.strptime("2001-01-01", "%Y-%m-%d").date(),
        html = "<h1>Hello</h1>",
        apply_url = "https://antinaho.com/apply"
    )