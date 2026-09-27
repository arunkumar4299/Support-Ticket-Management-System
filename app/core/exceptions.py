from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException):
        return JSONResponse(status_code=exc.status_code, content={
            "success": False,
            "error": {"code": "HTTP_ERROR", "message": str(exc.detail)}
        })

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=422, content={
            "success": False,
            "error": {"code": "VALIDATION_ERROR", "message": "Request validation failed", "details": exc.errors()}
        })

    @app.exception_handler(Exception)
    async def unhandled_error(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": {"code": "INTERNAL_SERVER_ERROR", "message": "Internal server error"}
        })
