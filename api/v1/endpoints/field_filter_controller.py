from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.field_filter_schema import FieldFilterCreate, FieldFilterOut
from services.field_filter_service import create_field_filter, toggle_filter_status, get_field_filters_for_site, \
    create_default_field_filter
from db.session import get_db

router = APIRouter()

# Crear un nuevo filtro de campos para un sitio
@router.post("/sites/{site_id}/field_filters/", response_model=FieldFilterOut)
def add_field_filter(site_id: int, filter_data: FieldFilterCreate, user_id: int, db: Session = Depends(get_db)):
    return create_field_filter(db, site_id, filter_data, user_id)

# Activar/Desactivar un filtro de campos
@router.put("/field_filters/{filter_id}/toggle/", response_model=FieldFilterOut)
def toggle_field_filter(filter_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        return toggle_filter_status(db, filter_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener todos los filtros de campos para un sitio
@router.get("/sites/{site_id}/field_filters/", response_model=list[FieldFilterOut])
def list_field_filters(site_id: int, db: Session = Depends(get_db)):
    return get_field_filters_for_site(db, site_id)

@router.post("/field_filters/default/", response_model=dict)
def add_default_field_filter(filter_data: FieldFilterCreate, user_id: int, db: Session = Depends(get_db)):
    try:
        return create_default_field_filter(db, filter_data.filter_key, user_id, filter_data.iterable)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))