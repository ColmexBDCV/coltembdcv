from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.article_filter_schema import ArticleFilterCreate, ArticleFilterOut
from services.article_filter_service import create_article_filter, toggle_article_filter_status, \
    get_article_filters_for_site, create_default_article_filter
from db.session import get_db

router = APIRouter()

# Crear un nuevo filtro de artículos
@router.post("/{site_id}/article_filters/", response_model=ArticleFilterOut)
def add_article_filter(site_id: int, filter_data: ArticleFilterCreate, user_id: int, db: Session = Depends(get_db)):
    return create_article_filter(db, site_id, filter_data, user_id)

# Activar/Desactivar un filtro de artículos
@router.put("/{filter_id}/toggle/", response_model=ArticleFilterOut)
def toggle_article_filter(filter_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        return toggle_article_filter_status(db, filter_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener todos los filtros de artículos para un sitio
@router.get("/{site_id}/article_filters/", response_model=list[ArticleFilterOut])
def list_article_filters(site_id: int, db: Session = Depends(get_db)):
    return get_article_filters_for_site(db, site_id)

# Crear un nuevo filtro de artículos por defecto y aplicarlo a todos los sitios (apagado por defecto)
@router.post("/article_filters/default/", response_model=dict)
def add_default_article_filter(filter_data: ArticleFilterCreate, user_id: int, db: Session = Depends(get_db)):
    try:
        return create_default_article_filter(db, filter_data.filter_key, user_id, filter_data.iterable)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))