from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.metadatasite_schema import MetadataSite, MetadataSiteCreate, MetadataSiteUpdate, MetadataSiteRequest
from services.metadatasite_service import (
    create_metadata_site,
    get_metadata_sites,
    get_metadata_site,
    update_metadata_site,
    delete_metadata_site
)
from db.session import get_db

router = APIRouter()

@router.post("/", response_model=MetadataSite)
def create_metadata_site_endpoint(
    metadata_site: MetadataSiteCreate, db: Session = Depends(get_db)
):
    return create_metadata_site(db, metadata_site)

@router.post("/metadataregister", response_model=list[MetadataSite])
def read_metadata_sites(request: MetadataSiteRequest, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_metadata_sites(db, id_site=request.id_site, id_registro=request.id_registro, skip=skip, limit=limit)

@router.get("/{metadata_site_id}", response_model=MetadataSite)
def read_metadata_site(metadata_site_id: int, db: Session = Depends(get_db)):
    db_metadata_site = get_metadata_site(db, metadata_site_id)
    if not db_metadata_site:
        raise HTTPException(status_code=404, detail="MetadataSite not found")
    return db_metadata_site

@router.put("/{metadata_site_id}", response_model=MetadataSite)
def update_metadata_site_endpoint(
    metadata_site_id: int, metadata_site_update: MetadataSiteUpdate, db: Session = Depends(get_db)
):
    db_metadata_site = get_metadata_site(db, metadata_site_id)
    if not db_metadata_site:
        raise HTTPException(status_code=404, detail="MetadataSite not found")
    return update_metadata_site(db, db_metadata_site, metadata_site_update)

@router.delete("/{metadata_site_id}", response_model=MetadataSite)
def delete_metadata_site_endpoint(metadata_site_id: int, db: Session = Depends(get_db)):
    db_metadata_site = delete_metadata_site(db, metadata_site_id)
    if not db_metadata_site:
        raise HTTPException(status_code=404, detail="MetadataSite not found")
    return db_metadata_site
