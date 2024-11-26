from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.metadata_schema import Metadatos, MetadatosCreate, MetadatosUpdate
from services.metadata_service import (
    create_metadato,
    get_metadatos,
    get_metadato,
    update_metadato,
    delete_metadato
)
from db.session import get_db

router = APIRouter()

@router.post("/", response_model=Metadatos)
def create_metadato_endpoint(
    metadato: MetadatosCreate, db: Session = Depends(get_db)
):
    return create_metadato(db, metadato)

@router.get("/", response_model=list[Metadatos])
def read_metadatos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_metadatos(db, skip=skip, limit=limit)

@router.get("/{metadato_id}", response_model=Metadatos)
def read_metadato(metadato_id: int, db: Session = Depends(get_db)):
    db_metadato = get_metadato(db, metadato_id)
    if not db_metadato:
        raise HTTPException(status_code=404, detail="Metadato not found")
    return db_metadato

@router.put("/{metadato_id}", response_model=Metadatos)
def update_metadato_endpoint(
    metadato_id: int, metadato_update: MetadatosUpdate, db: Session = Depends(get_db)
):
    db_metadato = get_metadato(db, metadato_id)
    if not db_metadato:
        raise HTTPException(status_code=404, detail="Metadato not found")
    return update_metadato(db, db_metadato, metadato_update)

@router.delete("/{metadato_id}", response_model=Metadatos)
def delete_metadato_endpoint(metadato_id: int, db: Session = Depends(get_db)):
    db_metadato = delete_metadato(db, metadato_id)
    if not db_metadato:
        raise HTTPException(status_code=404, detail="Metadato not found")
    return db_metadato
