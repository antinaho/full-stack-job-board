from backend.database.core import Base
from sqlalchemy import Column, String, Date, Text, Integer


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)

    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)

    added_on = Column(Date, nullable=False)
    html = Column(Text, nullable=False)
    apply_url = Column(String(500), nullable=False)

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"
