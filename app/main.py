import sqlalchemy

from utils.app_exceptions import AppExceptionCase
from fastapi import FastAPI, Request, Header
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


from routers import company, building, device, manager
from config.database import create_tables
import config.settings as settings

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from utils.app_exceptions import app_exception_handler
from config.database import session
from models.company import Company
from models.manager import Manager


# -------------------------------- Finished imports ------------------------------- #

app = FastAPI()
settings.init() # this file stores global settings/params

app.include_router(company.router)
app.include_router(manager.router)
app.include_router(building.router)
app.include_router(device.router)

@app.on_event("startup") # THIS IS VERY IMPORTANT! If we run create_tables outside this def pytest will not work!
async def startup_event():
    # ------------------------------- Create tables ------------------------------ #
    create_tables()

    # --------------------------- Add a superadmin user to db --------------------------- #
    try:
        company = Company(name = "seccom", address = "", phone = "")
        manager = Manager(idp_id = "f1034b00-29db-4004-acce-6b05ff1fbbb9", permissions = 4, company_id = 1)

        session.add(company)
        session.commit()
        session.refresh(company)

        session.add(manager)
        session.commit()
        session.refresh(manager)
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        session.rollback()
    # ---------------------------------------------------------------------------- #



# ----------------------------- add CORS headers ----------------------------- #
origins = ["*"] # "*" -> all origins

app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
