from pydantic import BaseModel
from datetime import datetime
from .user_auth_schema import UserAuth  # Asegúrate de tener un esquema para UserAuth

class MetadatosBase(BaseModel):
    nombre: str

class MetadatosCreate(MetadatosBase):
    usuario_id: int  # Relación directa con UserAuth

class MetadatosUpdate(MetadatosBase):
    pass

class MetadatosInDBBase(MetadatosBase):
    id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    usuario: UserAuth  # Incluye la relación con UserAuth

    class Config:
        orm_mode = True

class Metadatos(MetadatosInDBBase):
    pass
