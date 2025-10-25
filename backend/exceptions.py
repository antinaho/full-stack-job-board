from fastapi import HTTPException

class JobError(HTTPException):
    pass

class JobNotFoundError(JobError):
    def __init__(self, job_id=None):
        message = "Job not found" if job_id is None else f"Job with id {job_id} not found"
        super().__init__(status_code=404, detail=message)

class JobCreationError(JobError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create job: {error}")

class JobDateNotParsableError(JobError):
    def __init__(self, error: str):
        super().__init__(status_code=400, detail=f"Malformed query string: {error}")
