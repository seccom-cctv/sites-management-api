from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    address = Column(String(255), unique=True, index=False)
    phone = Column(String(30), unique=True, index=False)
    email = Column(String(255), unique=True, index=False)

    buildings = relationship("Building", back_populates="company")
    administrators = relationship("Administrator", back_populates="company")

class Administrator(Base):
    __tablename__ = "administrators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    phone = Column(String(30), unique=True, index=False)
    email = Column(String(255), unique=True, index=False)
    hashed_password = Column(String(255))
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="administrators")

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    address = Column(String(255), unique=True, index=False)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="buildings")
    devices = relationship("Device", back_populates="building")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    type = Column(String(255), unique=False, index=False)
    building_id = Column(Integer, ForeignKey("buildings.id"))

    building = relationship("Building", back_populates="devices")