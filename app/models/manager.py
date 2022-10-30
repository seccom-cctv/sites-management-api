from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.custom_types import JSONEncodedDict

from app.config.database import Base

class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    phone = Column(String(30), unique=True, index=False)
    email = Column(String(255), unique=True, index=False)
    hashed_password = Column(String(255))
    preferences = Column(JSONEncodedDict(), default={"notifications": {"from": ["alarms", "cameras"], "to": ["email", "sms"]}})
    permissions = Column(Integer, default=0)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="managers")