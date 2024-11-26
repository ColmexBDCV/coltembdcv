# models/map_model.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.base import Base


class Map(Base):
    __tablename__ = "maps"

    id = Column(Integer, primary_key=True, index=True)
    facet = Column(String, nullable=False)
    facet_value = Column(String, nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    active = Column(Boolean, default=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user_auth.id'), nullable=False)

    site = relationship("Site", back_populates="maps")
    user = relationship("UserAuth", back_populates="maps")
