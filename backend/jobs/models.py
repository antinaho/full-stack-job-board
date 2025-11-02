from pydantic import BaseModel, ConfigDict


class JobResponse(BaseModel):
    company_name: str
    job_title: str
    apply_url: str

    model_config = ConfigDict(from_attributes=True)


class JobCreate(BaseModel):
    job_title: str
    company_name: str
    apply_url: str
    html: str

    model_config = ConfigDict(from_attributes=True)


class JobDelete(BaseModel):
    id: int
    message: str = "Job deleted successfully"
