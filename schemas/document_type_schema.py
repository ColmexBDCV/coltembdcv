from pydantic import BaseModel
from datetime import datetime

class DocumentTypeBase(BaseModel):
    type_name: str
    type: str
    activo: bool

class DocumentTypeCreate(DocumentTypeBase):
    pass

class DocumentTypeOut(DocumentTypeBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
