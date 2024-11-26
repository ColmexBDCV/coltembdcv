from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base

class MetadataSite(Base):
    __tablename__ = "metadata_site"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(String, nullable=False)
    id_metadato = Column(Integer, ForeignKey("metadata.id"), nullable=False)  # Relación con Metadatos
    id_site = Column(Integer, ForeignKey("sites.id"), nullable=False)  # Relación con Site
    id_registro = Column(String, nullable=False)  # Campo string sin relación
    tipo = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("user_auth.id"), nullable=False)  # Relación con UserAuth

    # Relaciones con otros modelos
    metadatas = relationship("Metadata", back_populates="metadata_sites")
    site = relationship("Site", back_populates="metadata_sites")
    usuario = relationship("UserAuth")  # Relación con UserAuth
