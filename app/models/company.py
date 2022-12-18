from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    address = Column(String(255), unique=False, index=False)
    phone = Column(String(30), unique=True, index=False)
    email = Column(String(255), unique=True, nullable=True, index=False)

    buildings = relationship("Building", back_populates="company")
    managers = relationship("Manager", back_populates="company")

    def __repr__(self):
        return f"Company(id={self.id}, name={self.name}, address={self.address}, phone={self.phone}, email={self.email})"