# models/map_filter_model.py
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.base import Base


class MapFilter(Base):
    __tablename__ = "map_filters"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    id_filter_map_default = Column(Integer, ForeignKey("default_map_filters.id"), nullable=False)
    active = Column(Boolean, default=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user_auth.id'), nullable=False)

    site = relationship("Site", back_populates="map_filters")
    default_filter = relationship("DefaultMapFilter", back_populates="map_filters")
    user = relationship("UserAuth")
