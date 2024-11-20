from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    collection = Column(String, index=True, nullable=False)
    repository_url = Column(String, nullable=False)
    base_url = Column(String, nullable=False)
    link_url = Column(String, nullable=True)
    contacto_webhook = Column(String, nullable=False)
    monitor_webhook = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user_auth.id'),
                     nullable=False)  # Referencia al usuario que hizo la última modificación

    user = relationship("UserAuth")  # Relación con la tabla de autenticación

    # Relación con los filtros
    field_filters = relationship("FieldFilter", back_populates="site")
    facet_filters = relationship("FacetFilter", back_populates="site")
    article_filters = relationship("ArticleFilter", back_populates="site")
    maps = relationship("Map", back_populates="site")
    map_filters = relationship("MapFilter", back_populates="site")