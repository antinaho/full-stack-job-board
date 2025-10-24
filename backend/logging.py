from enum import StrEnum
import logging

class SeverityLevel(StrEnum):
    FATAL = "FATAL"
    ERRRO = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"

def setup_logging(severity_level: str = SeverityLevel.INFO):

    logging.basicConfig(
        level=severity_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )