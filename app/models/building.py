from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    address = Column(String(255), unique=True, index=False)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="buildings")
    devices = relationship("Device", back_populates="building")

    def __repr__(self):
        return f"Building(id={self.id}, name={self.name}, address={self.address}, company_id={self.company_id})"