from app.utils.app_exceptions import AppExceptionCase
from fastapi import FastAPI, Request, Header
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt


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

app.include_router(company.router)
app.include_router(manager.router)
app.include_router(building.router)
app.include_router(device.router)

@app.on_event("startup") # THIS IS VERY IMPORTANT! If we run create_tables outside this def pytest will not work!
async def startup_event():
    create_tables()

# ----------------------------- add CORS headers ----------------------------- #
origins = ["*"] # "*" -> all origins

app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# -------------------------------- Middleware -------------------------------- #
@app.middleware("http")
async def process_oidc_jwt(request: Request, call_next):
    headers = dict(request.headers)

    if "authorization" in headers:
        encoded_jwt = headers["authorization"].split("Bearer ")[1]
        payload = jwt.decode(encoded_jwt, key=None, algorithms=["RS256"], options={"verify_signature":False})
        print(payload)

    response = await call_next(request)
    return response

# ------------------- root path -> redirect to swagger docs ------------------ #
@app.get("/")
async def root():
    return RedirectResponse(url='/docs')


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)
