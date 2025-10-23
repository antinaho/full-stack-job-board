from pydantic import BaseModel, ConfigDict
from typing import Optional

class JobBase(BaseModel):
    pass

class JobResponse(JobBase):
    company_name: str
    job_title: str
    apply_url: str

class JobCreate(JobBase):
    job_title: str
    company_name: str
    apply_url: str
    html: str

    model_config = ConfigDict(from_attributes=True)
