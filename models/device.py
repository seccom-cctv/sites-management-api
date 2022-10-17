from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    type = Column(String(255), unique=False, index=False)
    building_id = Column(Integer, ForeignKey("buildings.id"))

    building = relationship("Building", back_populates="devices")