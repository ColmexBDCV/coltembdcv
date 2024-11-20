import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Site
from schemas.site_schemas import SiteCreate, SiteOut
from services.filter_service import get_field_filters, get_facet_filters, get_article_filters
from services.site_service import create_site, get_all_sites, get_site_by_id
from db.session import get_db
from utils.filter_logic import filter_data

router = APIRouter()

# Crear un nuevo sitio
@router.post("/sites/", response_model=SiteOut, summary="Creacion de un nuevo sitio", description="Se envian los datos necesarios para la creacion de un nuevo sitio")
def create_new_site(site_data: SiteCreate, user_id: int, db: Session = Depends(get_db)):
    try:
        return create_site(db, site_data, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Listar todos los sitios
@router.get("/sites/")
def list_all_sites(db: Session = Depends(get_db)):
    return get_all_sites(db)

# Obtener un sitio por su ID
@router.get("/sites/{site_id}")
def get_site(site_id: int, db: Session = Depends(get_db)):
    site = get_site_by_id(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


@router.get("/sites/{site_id}/fetch-data")
def fetch_site_data(site_id: int, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()

    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # Obtener los filtros activos para el sitio
    field_filters = get_field_filters(db, site_id)
    facet_filters = get_facet_filters(db, site_id)
    article_filters = get_article_filters(db, site_id)

    # Hacer la petición a la URL del sitio
    try:
        response = requests.get(site.repository_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from site: {e}")

    # Filtrar los datos obtenidos usando los filtros
    filtered_data = filter_data(data, field_filters, facet_filters, article_filters)

    return {"site": site, "data": filtered_data}