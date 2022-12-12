from urllib import response
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.config.database import Base, get_db
from app.main_for_testing import app
from app.models.device import Device

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

def test_post_a_device(test_db):
    response = client.post(
        "v1/device/",
        json={
        "name": "Camera A",
        "type": "Type X",
        "building_id": 9})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Camera A",
        "type": "Type X",
        "building_id": 9}

def test_update_device(test_db):
    json={
        "name": "Camera A",
        "type": "Type X",
        "building_id": 9}

    db = next(override_get_db())
    device = Device(**json)
    try:
        db.add(device)
        db.commit()
        db.refresh(device)
    except SQLAlchemyError as e:
        return str(e)
    
    id = 1
    response = client.put(f"v1/device/{id}",json={
        "name": "Camera BY",
        "type": "Type XZ",
        "building_id": 10})
    assert response.status_code == 200
    assert response.json() == {
        "id":1,
        "name": "Camera BY",
        "type": "Type XZ",
        "building_id": 10}

def test_get_device_by_id(test_db):
    json={
        "name": "Camera A",
        "type": "Type X",
        "building_id": 9}

    db = next(override_get_db())
    device = Device(**json)
    try:
        db.add(device)
        db.commit()
        db.refresh(device)
    except SQLAlchemyError as e:
        return str(e)
    
    id = 1
    response = client.get(f"v1/device/?id={id}")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "name": "Camera A",
        "type": "Type X",
        "building_id": 9}]

def test_get_device_by_building_id(test_db):
    json={
        "name": "Camera A",
        "type": "Type X",
        "building_id": 9}

    db = next(override_get_db())
    device = Device(**json)
    try:
        db.add(device)
        db.commit()
        db.refresh(device)
    except SQLAlchemyError as e:
        return str(e)
    
    id = 9
    response = client.get(f"v1/device/?building_id={id}")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "name": "Camera A",
        "type": "Type X",
        "building_id": 9}]

def test_delete_device(test_db):
    json={
        "name": "Camera A",
        "type": "Type X",
        "building_id": 9}

    db = next(override_get_db())
    company = Device(**json)
    try:
        db.add(company)
        db.commit()
        db.refresh(company)
    except SQLAlchemyError as e:
        return str(e)

    id=1
    response = client.delete(f"v1/device/{id}")
    assert response.status_code == 200
    assert response.json() == {"deleted_rows": 1}
    