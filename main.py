from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from src.app.api.errors.http_error import http_error_handler
from src.app.api.errors.validation_error import http422_error_handler
from src.app.api.routes.api import router as api_router


def get_application() -> FastAPI:

    application = FastAPI(title="Orchestrator")

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router)

    return application


app = get_application()
