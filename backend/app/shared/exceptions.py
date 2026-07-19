from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger("app")

class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, errors: list = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []

def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "errors": exc.errors
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTPException: {exc.detail} on path {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "errors": []
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation error on path {request.url.path}: {exc.errors()}")
        errors_list = []
        for error in exc.errors():
            loc = " -> ".join(str(x) for x in error["loc"])
            errors_list.append({
                "field": loc,
                "message": error["msg"]
            })
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": "Validation failed",
                "errors": errors_list
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)} on path {request.url.path}", exc_info=True)
        
        from app.config.settings import settings
        import traceback
        
        content = {
            "success": False,
            "message": "Internal server error occurred",
            "errors": []
        }
        
        if settings.ENVIRONMENT.lower() != "production":
            content["message"] = f"Debug: {exc.__class__.__name__}: {str(exc)}"
            content["errors"] = traceback.format_exception(type(exc), exc, exc.__traceback__)
            
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=content
        )

