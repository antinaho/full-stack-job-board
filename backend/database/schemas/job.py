from backend.database.core import Base
from sqlalchemy import Column, String, Date, Integer

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    company_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    
    added_on = Column(Date, nullable=False)
    html = Column(String, nullable=False)
    apply_url = Column(String, nullable=False)

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"