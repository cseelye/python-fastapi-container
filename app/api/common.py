from datetime import datetime
import json
import random
import string
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from pydantic import BaseModel

from app.util.log import log


# Tags to make the swagger UI look nicer and sort/separate the API versions
# Add a new tag for each endpoint version
version_tags = [{"name": "v1", "description": "Version 1 APIs"}, {"name": "v2", "description": "Version 2 APIs"}]


##############################################################################
# Error schema
##############################################################################
class ErrorResponse(BaseModel):
    """Schema for all errors returned from the API"""

    message: str
    errorCode: int = 999
    detail: dict = {}

    class Config:
        fields = {
            "message": {"description": "A human readable error message summarizing the problem"},
            "errorCode": {"description": "A machine readable error code unique to this error"},
            "detail": {"description": "Object with more information about the error"},
        }


# List of common error responses - all APIs should use this
responses = {
    500: {"description": "Application Error", "model": ErrorResponse},
    422: {"description": "Validation Error", "model": ErrorResponse},
}


##############################################################################
# Request/response logging
##############################################################################
async def log_request(r_id: str, request: Request):
    """Helper for logging an API request"""
    try:
        body = await request.json()
    except json.JSONDecodeError:
        body = (await request.body()).decode("utf-8")
    log.debug(
        f"Starting request id=[{r_id}] client=[{request.client.host}:{request.client.port}] url=[{request.url}] method=[{request.method}] params=[{request.path_params}] body=[{body}]"
    )


async def log_response(r_id: str, response: Response, elapsed: float):
    """Helper for logging an API response"""
    msg = f"Finished request id=[{r_id}] time=[{elapsed}] status_code=[{response.status_code}]"
    if response.status_code == 200:
        body_str = (
            (response.body[:900].decode("utf-8") + " (..truncated)")
            if len(response.body) > 1024
            else response.body.decode("utf-8")
        )
        msg += f" response=[{body_str}]"
    log.debug(msg)


class LoggedRoute(APIRoute):
    """This class adds logging of the API request/response along with elapsed time"""

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            r_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            await log_request(r_id, request)
            start = datetime.now()
            response: Response = await original_route_handler(request)
            end = datetime.now()
            elapsed = float((end - start).seconds) + float((end - start).microseconds) / 1000000.0
            await log_response(r_id, response, elapsed)
            return response

        return custom_route_handler
