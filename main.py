from fastapi import FastAPI, Request, Response
from routers import company
from config.database import create_tables

create_tables()
app = FastAPI()

app.include_router(company.router)

@app.get("/")
async def read_root():
    '''Document endpoint usage here'''
    return {"Hello": "World"}