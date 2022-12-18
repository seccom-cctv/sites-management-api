from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.custom_types import JSONEncodedDict

from config.database import Base

class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, index=True)
    idp_id = Column(String(255), unique=True, index=True)
    preferences = Column(JSONEncodedDict(), default={"notifications": {"from": ["alarms", "cameras"], "to": ["email", "sms"]}})
    permissions = Column(Integer, default=0) # 0 = client; 4 = superadmin
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="managers")