from pydantic import BaseModel
from typing import List, Optional

class FilterItem(BaseModel):
    key: str
    value: str

class ModalFacetRequest(BaseModel):
    facet_label: str
    facet_sort: str
    facet_page: int
    filters: List[FilterItem]
    search: Optional[str] = ''
