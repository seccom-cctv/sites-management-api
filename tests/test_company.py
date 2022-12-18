from urllib import response
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from config.database import Base, get_db
from main import app
from models.company import Company

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Testing Routers

def test_post_a_company(test_db):
    response = client.post(
        "v1/company/",
        json={
        "name": "Company A",
        "address": "Address X",
        "phone": "918276234",
        "email": "m@ua.pt"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Company A",
        "address": "Address X",
        "phone": "918276234",
        "email": "m@ua.pt"}

def test_update_company(test_db):
    json={
        "name": "Company A",
        "address": "Address XYZ",
        "phone": "918276234",
        "email": "m@ua.pt"}

    db = next(override_get_db())
    company = Company(**json)
    try:
        db.add(company)
        db.commit()
        db.refresh(company)
    except SQLAlchemyError as e:
        return str(e)
    
    id = 1
    response = client.put(f"v1/company/{id}",json={
        "name": "Company A",
        "address": "Address XYZ",
        "phone": "918276635",
        "email": "m@ua.pt"})
    assert response.status_code == 200
    assert response.json() == {
        "id":1,
        "name": "Company A",
        "address": "Address XYZ",
        "phone": "918276635",
        "email": "m@ua.pt"}

def test_get_company(test_db):
    json={
        "name": "Company A",
        "address": "Address X",
        "phone": "918276234",
        "email": "m@ua.pt"}

    db = next(override_get_db())
    company = Company(**json)
    try:
        db.add(company)
        db.commit()
        db.refresh(company)
    except SQLAlchemyError as e:
        return str(e)
    
    id = 1
    response = client.get(f"v1/company/?id={id}")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "name": "Company A",
        "address": "Address X",
        "phone": "918276234",
        "email": "m@ua.pt"}]

def test_delete_company(test_db):
    json={
        "name": "Company A",
        "address": "Address X",
        "phone": "918276234",
        "email": "m@ua.pt"}

    db = next(override_get_db())
    company = Company(**json)
    try:
        db.add(company)
        db.commit()
        db.refresh(company)
    except SQLAlchemyError as e:
        return str(e)

    id=1
    response = client.delete(f"v1/company/{id}")
    assert response.status_code == 200
    assert response.json() == {"deleted_rows": 1}
    