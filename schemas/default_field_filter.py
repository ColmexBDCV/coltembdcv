from pydantic import BaseModel

# Esquema base con los campos comunes
class DefaultFieldFilterBase(BaseModel):
    filter_key: str
    iterable: bool

# Esquema para la creación
class DefaultFieldFilterCreate(DefaultFieldFilterBase):
    pass

# Esquema para la salida
class DefaultFieldFilterOut(DefaultFieldFilterBase):
    id: int

    class Config:
        from_attributes = True  # Permite trabajar con objetos SQLAlchemy