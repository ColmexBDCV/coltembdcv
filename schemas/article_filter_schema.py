from pydantic import BaseModel
from datetime import datetime

class ArticleFilterBase(BaseModel):
    filter_key: str
    active: bool
    iterable: bool

class ArticleFilterCreate(ArticleFilterBase):
    pass

class ArticleFilterOut(ArticleFilterBase):
    id: int
    site_id: int
    user_id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
