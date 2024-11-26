from pydantic import BaseModel
from datetime import datetime
from .metadata_schema import MetadatosInDBBase

class MetadataSiteBase(BaseModel):
    valor: str
    id_metadato: int
    id_site: int
    id_registro: str
    tipo: str

class MetadataSiteCreate(MetadataSiteBase):
    usuario_id: int

class MetadataSiteUpdate(MetadataSiteBase):
    pass

class MetadataSiteInDBBase(MetadataSiteBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    usuario_id: int
    metadatas: MetadatosInDBBase

    class Config:
        orm_mode = True

class MetadataSite(MetadataSiteInDBBase):
    pass

class MetadataSiteRequest(BaseModel):
    id_site: int
    id_registro: str
    skip: int = 0
    limit: int = 100