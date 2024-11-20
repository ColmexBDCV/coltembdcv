from pydantic import BaseModel
from datetime import datetime

class FacetFilterBase(BaseModel):
    filter_key: str
    active: bool

class FacetFilterCreate(FacetFilterBase):
    pass

class FacetFilterOut(FacetFilterBase):
    id: int
    site_id: int
    user_id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
