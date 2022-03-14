"""
Implementation of v1 API endpoints
"""

from fastapi import APIRouter
import functools
import inspect
from subprocess import TimeoutExpired
from datetime import datetime

from app.util import get_service_version
from app.util.shell import execute_command
from app.exceptions import AppException, ErrorCode
from . import schemas
from ..common import responses, LoggedRoute

##############################################################################
# Temporarily disabled APIs
##############################################################################
DISABLED_APIS = []

##############################################################################
# Declare the router for this endpoint
##############################################################################
v1_router = APIRouter(prefix="/v1", route_class=LoggedRoute)  # Use the API version as the endpoint prefix


def add_api(endpoint, impl, method, response, visible=True, tags=None):
    """Helper function to add an API method to this endpoint"""

    @functools.wraps(impl)
    async def checked_impl(*args, **kwargs):
        check_enabled(endpoint, method)
        if inspect.isawaitable(impl):
            return await impl(*args, **kwargs)
        else:
            return impl(*args, **kwargs)

    api_tags = ["v2"]
    if tags:
        api_tags += tags

    v1_router.add_api_route(
        endpoint,
        checked_impl,
        methods=[method],
        response_model=response,
        responses=responses,
        tags=api_tags,
        include_in_schema=visible and check_enabled(endpoint, method, throw=False),
    )


def check_enabled(endpoint, method, throw=True):
    """Check if an API call is enabled on this platform"""
    enabled = True
    if (endpoint, method) in DISABLED_APIS:
        enabled = False

    if not enabled and throw:
        raise AppException(
            "This API is not available on this platform",
            code=ErrorCode.DisabledApi,
            detail={"resource": endpoint, "method": method},
        )
    return enabled


##############################################################################
# API implementation functions
##############################################################################
def about():
    """
    Get basic information about this service
    """
    return schemas.AboutService(version=get_service_version())


def run_command(cmd: schemas.CommandSpec):
    """
    Run a command on this server
    """
    try:
        start = datetime.now()
        return_code, stdout, stderr = execute_command(cmd.commandline, timeout=cmd.timeout)
        end = datetime.now()
    except TimeoutExpired:
        raise AppException(
            "Command timed out",
            detail={"command": cmd.commandline, "timeout": cmd.timeout},
        ) from None

    return schemas.CommandResponse(
        return_code=return_code,
        stdout=stdout,
        stderr=stderr,
        elapsed_time=float((end - start).seconds) + float((end - start).microseconds) / 1000000.0,
    )


##############################################################################
# Define the API by attaching the API function to endpoints on the router
##############################################################################
add_api("/about", about, method="GET", response=schemas.AboutService)
add_api("/command", run_command, method="POST", response=schemas.CommandResponse)
