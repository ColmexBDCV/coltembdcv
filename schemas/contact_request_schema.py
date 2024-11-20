from pydantic import BaseModel

class ContactRequest(BaseModel):
    mail: str
    asunto: str
    mensaje: str