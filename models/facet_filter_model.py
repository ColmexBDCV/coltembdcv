from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class FacetFilter(Base):
    __tablename__ = "facet_filters"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('sites.id'))
    filter_key = Column(String, index=True, nullable=False)
    active = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user_auth.id'), nullable=False)

    site = relationship("Site", back_populates="facet_filters")
    user = relationship("UserAuth")
