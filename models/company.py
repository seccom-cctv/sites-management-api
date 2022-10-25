from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    address = Column(String(255), unique=True, index=False)
    phone = Column(String(30), unique=True, index=False)
    email = Column(String(255), unique=True, nullable=True, index=False)

    buildings = relationship("Building", back_populates="company")
    administrators = relationship("Administrator", back_populates="company")