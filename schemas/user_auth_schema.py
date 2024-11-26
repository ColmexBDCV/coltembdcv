from pydantic import BaseModel

class UserAuthBase(BaseModel):
    username: str

class UserAuthCreate(UserAuthBase):
    password: str  # Contraseña en texto plano, que será cifrada

class UserAuthOut(UserAuthBase):
    id: int

    class Config:
        from_attributes = True

class UserAuth(UserAuthOut):
    pass
