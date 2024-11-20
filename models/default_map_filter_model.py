# models/default_map_filter_model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base

class DefaultMapFilter(Base):
    __tablename__ = "default_map_filters"

    id = Column(Integer, primary_key=True, index=True)
    filter_key = Column(String, unique=True, nullable=False)

    map_filters = relationship("MapFilter", back_populates="default_filter")
