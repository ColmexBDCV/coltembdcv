from pydantic import BaseModel

class SiteCreate(BaseModel):
    name: str
    repository_url: str
    base_url: str
    link_url: str

class SiteOut(SiteCreate):
    id: int

    class Config:
        from_attributes = True