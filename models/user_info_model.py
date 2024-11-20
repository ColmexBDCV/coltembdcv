from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido_paterno = Column(String, nullable=False)
    apellido_materno = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_auth_id = Column(Integer, ForeignKey('user_auth.id'), nullable=False)
    user_auth = relationship("UserAuth", back_populates="user_info")