from sqlalchemy import Column, Integer, String, Boolean
from db.base import Base

class DefaultFieldFilter(Base):
    __tablename__ = "default_field_filters"

    id = Column(Integer, primary_key=True, index=True)
    filter_key = Column(String, unique=True, nullable=False)  # Clave del filtro (ej: "handle")
    iterable = Column(Boolean, default=True)
