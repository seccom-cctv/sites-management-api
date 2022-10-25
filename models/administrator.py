from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base

class Administrator(Base):
    __tablename__ = "administrators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    phone = Column(String(30), unique=True, index=False)
    email = Column(String(255), unique=True, index=False)
    hashed_password = Column(String(255))
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="administrators")