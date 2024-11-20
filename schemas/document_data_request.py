from pydantic import BaseModel
from typing import Optional

class DocumentDataRequest(BaseModel):
    id: str
    has_model: str
    thumbnail: Optional[str] = None
    related: Optional[str] = None