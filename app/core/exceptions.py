import logging

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


def error_response(message: str):
    """
    Create the standard API error response format.
    """
    return {
        "data": None,
        "error": {
            "message": message,
        },
    }


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    """
    Handle FastAPI HTTP exceptions such as 404.
    """

    if isinstance(exc.detail, dict):
        response = exc.detail
    else:
        response = error_response(str(exc.detail))

    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    """
    Handle Pydantic/FastAPI validation errors.
    """

    errors = exc.errors()

    messages = []

    for error in errors:
        location = " -> ".join(str(item) for item in error["loc"])
        message = error["msg"]

        messages.append(
            f"{location}: {message}"
        )

    return JSONResponse(
        status_code=422,
        content=error_response(
            "; ".join(messages)
        ),
    )


async def general_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected server errors.

    Detailed error information is logged on the server,
    but is not exposed to the API client.
    """

    logger.exception(
        "Unhandled exception while processing request: %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content=error_response(
            "An unexpected server error occurred."
        ),
    )