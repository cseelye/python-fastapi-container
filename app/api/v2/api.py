"""
Implementation of v2 API endpoints

This sample shows several options for building a new version endpoint:
    Add new API
    Change the behavior of existing API but keep the old schema
    Copy an API from the older endpoint with identical behavior and inputs/outputs
"""

from fastapi import APIRouter

from app.util import get_service_version
from . import schemas as v2_schemas
from ..v1 import api as v1_api
from ..v1 import schemas as v1_schemas
from ..common import responses, LoggedRoute

##############################################################################
# Declare the router for this endpoint
##############################################################################
v2_router = APIRouter(prefix="/v2", route_class=LoggedRoute)  # Use the API version as the endpoint prefix


def add_api(endpoint, impl, method, response):
    """Helper function to add an API method to the v2 endpoint"""
    v2_router.add_api_route(
        endpoint,
        impl,
        methods=[method],
        response_model=response,
        responses=responses,
        tags=["v2"],
    )


##############################################################################
# API implementation functions
##############################################################################
async def health():
    return v2_schemas.HealthResponse(healthy=True)


async def about():
    return v1_schemas.AboutService(version=get_service_version(), service_name="New Improved Name")


##############################################################################
# Define the API by attaching the API function to endpoints on the router
##############################################################################

# /health is a new v2 endpoint only with new schema and new implementation
add_api("/health", health, method="GET", response=v2_schemas.HealthResponse)

# /about on v2 endpoint still uses the v1 schema, but new v2 implementation
add_api("/about", about, method="GET", response=v1_schemas.AboutService)

# /command on v2 endpoint uses the v1 schema and implementation so it is unchanged
add_api("/command", v1_api.run_command, method="POST", response=v1_schemas.CommandResponse)
