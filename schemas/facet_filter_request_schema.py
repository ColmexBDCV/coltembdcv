from pydantic import BaseModel


class FacetFilter(BaseModel):
    key: str
    value: str

class FilterRequest(BaseModel):
    facet: list[FacetFilter]