from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base

class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("user_auth.id"), nullable=False)  # Clave foránea hacia UserAuth

    # Relación con UserAuth
    usuario = relationship("UserAuth", back_populates="metadatos")
    metadata_sites = relationship("MetadataSite", back_populates="metadatas")
