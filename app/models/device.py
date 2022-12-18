from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=False, index=True)
    type = Column(String(255), unique=False, index=False)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    building = relationship("Building", back_populates="devices")

    def __repr__(self):
        return f"Device(id={self.id}, name={self.name}, type={self.type}, building_id={self.building_id})"
