from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    address = Column(String(255), unique=True, index=False)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="buildings")
    devices = relationship("Device", back_populates="building")