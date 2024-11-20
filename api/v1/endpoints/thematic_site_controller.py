import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.session import get_db
from models import Site, FieldFilter, FacetFilter, ArticleFilter, DocumentType
from schemas.document_data_request import DocumentDataRequest
from schemas.facet_filter_request_schema import FilterRequest
from schemas.modal_facet_schema import ModalFacetRequest
from services.map_service import build_url_with_filters
from services.thematic_service import get_document_data_service, build_facet_url, fetch_facet_data, is_next_page
from utils.filter_logic import filter_data

router = APIRouter()


@router.post("/{site_id}/filtered-data/")
def get_filtered_data(site_id: int, filters: FilterRequest, db: Session = Depends(get_db)):
    # Obtener el sitio desde la base de datos usando el site_id
    site = db.query(Site).filter(Site.id == site_id).first()

    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # Obtener la base_url del sitio
    base_url = site.repository_url

    # Construir la URL agregando los filtros de facet
    for facet in filters.facet:
        base_url += f"&f[{facet.key}][]={facet.value}"

    try:
        # Realizar la petición a la URL construida
        response = requests.get(base_url)
        response_data = response.json()

        # Obtener los filtros (field_filter, facet_filter, article_filter) desde la base de datos
        field_filters = db.query(FieldFilter).filter(FieldFilter.site_id == site_id, FieldFilter.active == True).all()
        facet_filters = db.query(FacetFilter).filter(FacetFilter.site_id == site_id, FacetFilter.active == True).all()
        article_filters = db.query(ArticleFilter).filter(ArticleFilter.site_id == site_id,
                                                         ArticleFilter.active == True).all()

        # Aplicar la lógica de filtrado
        filtered_data = filter_data(response_data, field_filters, facet_filters, article_filters)

        return {"site": site, "data": filtered_data}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from URL: {str(e)}")


@router.post("/{site_id}/search-data/")
def search_data(site_id: int, payload: dict, db: Session = Depends(get_db)):
    filters = payload.get("filters")
    search = payload.get("search")
    page = payload.get("page")
    search_in = payload.get("search_in")

    # Obtiene la información del sitio para extraer la base_url
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # Construye la URL base del sitio
    repository_url = site.repository_url

    # Si se incluye search, se agrega a la URL
    repository_url += f"&search_field={search_in}&q={search}"

    # Agrega los filtros en formato de URL
    for facet in filters.get("facet", []):
        repository_url += f"&f[{facet['key']}][]={facet['value']}"

    repository_url += f"&page={page}"

    # Realiza la petición a la URL construida
    try:
        response = requests.get(repository_url)
        data = response.json()  # Asume que la respuesta es JSON
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching data from repository: {str(e)}")

    # Aplica la lógica de filtrado a los datos obtenidos
    field_filters = db.query(FieldFilter).filter(FieldFilter.site_id == site_id).all()
    facet_filters = db.query(FacetFilter).filter(FacetFilter.site_id == site_id).all()
    article_filters = db.query(ArticleFilter).filter(ArticleFilter.site_id == site_id).all()

    filtered_data = filter_data(data, field_filters, facet_filters, article_filters)

    return {"site": site, "data": filtered_data}


@router.post("/{site_id}/document-data/")
def get_document_data(
        site_id: int,
        document_data: DocumentDataRequest,
        db: Session = Depends(get_db)
):
    try:
        data = get_document_data_service(db, site_id, document_data.dict())
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving document data")


@router.post("/{site_id}/facet-data/")
def get_facet_data(
        site_id: int,
        request_data: ModalFacetRequest,
        db: Session = Depends(get_db)
):
    # Obtener la información del sitio desde la BD
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    # Construir la URL y obtener los datos
    url = build_facet_url(
        site=site,
        facet_label=request_data.facet_label,
        facet_sort=request_data.facet_sort,
        facet_page=request_data.facet_page,
        filters=request_data.filters,
        search=request_data.search
    )

    data = fetch_facet_data(url)
    data["response"]["facets"]["isNextPage"] = is_next_page(site=site,
                                                            facet_label=request_data.facet_label,
                                                            facet_sort=request_data.facet_sort,
                                                            facet_page=request_data.facet_page,
                                                            filters=request_data.filters,
                                                            search=request_data.search)
    if data is None:
        raise HTTPException(status_code=500, detail="Error fetching facet data")

    return {"site": site, "data": data}

@router.get("/{site_id}/map_coords")
def get_map_coordinates(site_id: int, db: Session = Depends(get_db)):
    try:
        data = build_url_with_filters(db, site_id)

        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
