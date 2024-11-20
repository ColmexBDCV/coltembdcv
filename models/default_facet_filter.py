from sqlalchemy import Column, Integer, String
from db.base import Base

class DefaultFacetFilter(Base):
    __tablename__ = "default_facet_filters"

    id = Column(Integer, primary_key=True, index=True)
    filter_key = Column(String, unique=True, nullable=False)
