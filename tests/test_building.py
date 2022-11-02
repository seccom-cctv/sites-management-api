from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.config.database import Base, get_db
from app.main import app
from app.models.building import Building

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

def test_post_a_building(test_db):
    response = client.post(
        "v1/building/",
        json={
        "name": "Building X",
        "address": "Address X",
        "company_id": 1})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Building X",
        "address": "Address X",
        "company_id": 1}

def test_get_building_by_id(test_db):
    json={
        "name": "Building X",
        "address": "Address X",
        "company_id": 1}

    db = next(override_get_db())
    building = Building(**json)
    print(building, "building")
    try:
        db.add(building)
        db.commit()
        db.refresh(building)
    except SQLAlchemyError as e:
        return str(e)
    
    id=1
    response = client.get(f"v1/building/?id={id}")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "name": "Building X",
        "address": "Address X",
        "company_id": 1}]

def test_get_building_by_company_id(test_db):
    json={
        "name": "Building X",
        "address": "Address X",
        "company_id": 1}

    db = next(override_get_db())
    building = Building(**json)
    print(building, "building")
    try:
        db.add(building)
        db.commit()
        db.refresh(building)
    except SQLAlchemyError as e:
        return str(e)
    
    id=1
    response = client.get(f"v1/building/?company_id={id}")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "name": "Building X",
        "address": "Address X",
        "company_id": 1}]


def test_update_building(test_db):
    json={
        "name": "Building X",
        "address": "Address X",
        "company_id": 1}

    db = next(override_get_db())
    building = Building(**json)
    try:
        db.add(building)
        db.commit()
        db.refresh(building)
    except SQLAlchemyError as e:
        return str(e)
        
    id = 1
    response = client.put(f"v1/building/{id}",json={
        "name": "Building Y",
        "address": "Address XYZ",
        "company_id": 1})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Building Y",
        "address": "Address XYZ",
        "company_id": 1
    }

def test_delete_company(test_db):
    json={
        "name": "Building Y",
        "address": "Address XYZ",
        "company_id": 1}

    db = next(override_get_db())
    building = Building(**json)
    try:
        db.add(building)
        db.commit()
        db.refresh(building)
    except SQLAlchemyError as e:
        return str(e)

    id=1
    response = client.delete(f"v1/building/{id}")
    assert response.status_code == 200
    assert response.json() == {"deleted_rows": 1}

    
