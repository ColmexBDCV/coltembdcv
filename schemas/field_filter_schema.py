from pydantic import BaseModel
from datetime import datetime

class FieldFilterBase(BaseModel):
    filter_key: str
    iterable: bool
    active: bool

class FieldFilterCreate(FieldFilterBase):
    pass

class FieldFilterOut(FieldFilterBase):
    id: int
    site_id: int
    user_id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
