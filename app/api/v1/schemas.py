"""
Input/Output models for the V1 endpoint
"""

from pydantic import BaseModel


class AboutService(BaseModel):
    service_name: str = "TemplateService"
    version: str

    class Config:
        fields = {
            "service_name": {"description": "Human readable name of this service"},
            "version": {"description": "Current version of this service", "example": "YY.MM.VV"},
        }


class CommandSpec(BaseModel):
    commandline: str
    timeout: int = 300

    class Config:
        fields = {
            "commandline": {"description": "Command to execute", "example": "ls -la"},
            "timeout": {"description": "Timeout before failing and aborting the command"},
        }


class CommandResponse(BaseModel):
    return_code: int
    stdout: str
    stderr: str
    elapsed_time: float

    class Config:
        fields = {
            "return_code": {"description": "The return code of the command"},
            "stdout": {"description": "The output of the command"},
            "stderr": {"description": "The error output of the command"},
            "elapsed_time": {"description": "The time the command took to execute, in sec"},
        }
