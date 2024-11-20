from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.facet_filter_schema import FacetFilterCreate, FacetFilterOut
from services.facet_filter_service import create_facet_filter, toggle_facet_filter_status, get_facet_filters_for_site, \
    create_default_facet_filter
from db.session import get_db

router = APIRouter()

# Crear un nuevo filtro de facetas
@router.post("/sites/{site_id}/facet_filters/", response_model=FacetFilterOut)
def add_facet_filter(site_id: int, filter_data: FacetFilterCreate, user_id: int, db: Session = Depends(get_db)):
    return create_facet_filter(db, site_id, filter_data, user_id)

# Activar/Desactivar un filtro de facetas
@router.put("/facet_filters/{filter_id}/toggle/", response_model=FacetFilterOut)
def toggle_facet_filter(filter_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        return toggle_facet_filter_status(db, filter_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener todos los filtros de facetas para un sitio
@router.get("/sites/{site_id}/facet_filters/", response_model=list[FacetFilterOut])
def list_facet_filters(site_id: int, db: Session = Depends(get_db)):
    return get_facet_filters_for_site(db, site_id)

@router.post("/facet_filters/default/", response_model=dict)
def add_default_facet_filter(filter_data: FacetFilterCreate, user_id: int, db: Session = Depends(get_db)):
    try:
        return create_default_facet_filter(db, filter_data.filter_key, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))