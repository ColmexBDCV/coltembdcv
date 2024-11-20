from pydantic import BaseModel
from datetime import datetime

class UserInfoBase(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None
    email: str

class UserInfoCreate(UserInfoBase):
    pass

class UserInfoOut(UserInfoBase):
    id: int
    user_auth_id: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True
