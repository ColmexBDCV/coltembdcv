from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class DocumentType(Base):
    __tablename__ = "document_types"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, unique=True, nullable=False)  # Nombre descriptivo del tipo de documento
    type = Column(String, unique=True, nullable=False)  # Valor asociado al tipo (ej. 'articles', 'theses')
    fecha_creacion = Column(DateTime, default=datetime.utcnow)  # Fecha de creación
    fecha_modificacion = Column(DateTime, onupdate=datetime.utcnow)  # Fecha de modificación
    usuario_id = Column(Integer, ForeignKey('user_auth.id'))  # ID del usuario que crea o modifica
    usuario = relationship("UserAuth")  # Relación con el usuario
    activo = Column(Boolean, default=True)  # Indica si el tipo está activo
