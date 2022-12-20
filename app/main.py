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
        # client-web-ui cognito pool root user
        manager_client_pool = Manager(idp_id = "b99373ce-d903-4c9a-a0ab-ee192ca89731", permissions = 4, company_id = 1)
        # management-web-ui cognito pool root user
        manager_management_pool = Manager(idp_id = "75e1c506-86a9-44f7-8684-4ccc9c7a480a", permissions = 4, company_id = 1)

        session.add(company)
        session.commit()
        session.refresh(company)

        session.add(manager_client_pool)
        session.commit()
        session.refresh(manager_client_pool)

        session.add(manager_management_pool)
        session.commit()
        session.refresh(manager_management_pool)

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
