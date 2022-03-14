#!/usr/bin/env python3
"""
Main entry point for service
"""
import traceback

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.util.log import log
import app.api.v1 as api_v1
import app.api.v2 as api_v2
from app.api.common import ErrorResponse, version_tags
from app.exceptions import AppException
from app.util import get_service_version

##############################################################################
# App definition
##############################################################################
app = FastAPI(
    title="Example Service using FastAPI",
    description="Template project for containerized services using FastAPI",
    version=get_service_version(),
    openapi_tags=version_tags,
)

# Include the API versions we want to serve
log.info("Configuring endpoints")
app.include_router(api_v1.router)
app.include_router(api_v2.router)

##############################################################################
# Custom exception handlers
##############################################################################
@app.exception_handler(AppException)
def app_exception_handler(_request, ex):
    """
    Catch application errors and convert them to our structured error format
    """
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ErrorResponse(message=ex.message, errorCode=ex.code, detail=ex.detail)),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, ex):
    """
    Catch validation errors and convert them to our structured error format
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            ErrorResponse(
                message=f"Request Validation Error: {str(ex)}",
                errorCode=1,
                detail={"error": jsonable_encoder(ex.errors()), "body": ex.body},
            )
        ),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_request, ex):
    """
    Catch HTTP exceptions and convert them to our structured error format
    """
    return JSONResponse(
        status_code=ex.status_code,
        content=jsonable_encoder(ErrorResponse(message=ex.detail, errorCode=4, detail={})),
    )


@app.exception_handler(Exception)
def unhandled_exception_handler(_request, ex):
    """
    Catch any otherwise unhandled exceptions and convert them to our structured error format
    """
    lines = [ll for line in traceback.format_tb(ex.__traceback__) for ll in line.split("\n") if ll]
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            ErrorResponse(
                message=f"Uhandled exception: {str(ex) or '<empty message>'}",
                errorCode=999,
                detail={"type": ex.__class__.__name__, "traceback": lines},
            )
        ),
    )
