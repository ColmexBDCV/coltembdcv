from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base


class ArticleFilter(Base):
    __tablename__ = "article_filters"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey('sites.id'))
    filter_key = Column(String, index=True, nullable=False)
    active = Column(Boolean, default=True)
    iterable = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user_auth.id'), nullable=False)

    site = relationship("Site", back_populates="article_filters")
    user = relationship("UserAuth")
