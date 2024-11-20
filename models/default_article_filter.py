from sqlalchemy import Column, Integer, String, Boolean
from db.base import Base

class DefaultArticleFilter(Base):
    __tablename__ = "default_article_filters"

    id = Column(Integer, primary_key=True, index=True)
    filter_key = Column(String, unique=True, nullable=False)
    iterable = Column(Boolean, default=True)
