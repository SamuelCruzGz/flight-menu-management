from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.base import BusinessException


def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register all application exception handlers.
    """

    @app.exception_handler(BusinessException)
    async def business_exception_handler(
        request: Request,
        exc: BusinessException,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.message,
                    "type": exc.__class__.__name__,
                }
            },
        )