from app.utils.app_exceptions import AppExceptionCase
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import company, building, device, manager
from app.config.database import create_tables

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from app.utils.app_exceptions import app_exception_handler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(company.router)
app.include_router(manager.router)
app.include_router(building.router)
app.include_router(device.router)

@app.get("/")
async def root():
    return RedirectResponse(url='/docs')
