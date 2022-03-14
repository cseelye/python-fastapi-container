"""
Input/Output models for the V2 endpoint
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    healthy: bool
