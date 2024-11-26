from sqlalchemy.orm import Session
from models.metadata_model import Metadata
from schemas.metadata_schema import MetadatosCreate, MetadatosUpdate

def create_metadato(db: Session, metadato: MetadatosCreate):
    db_metadato = Metadata(**metadato.dict())
    db.add(db_metadato)
    db.commit()
    db.refresh(db_metadato)
    return db_metadato

def get_metadatos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Metadata).offset(skip).limit(limit).all()

def get_metadato(db: Session, metadato_id: int):
    return db.query(Metadata).filter(Metadata.id == metadato_id).first()

def update_metadato(db: Session, db_metadato: Metadata, metadato_update: MetadatosUpdate):
    for key, value in metadato_update.dict(exclude_unset=True).items():
        setattr(db_metadato, key, value)
    db.commit()
    db.refresh(db_metadato)
    return db_metadato

def delete_metadato(db: Session, metadato_id: int):
    db_metadato = db.query(Metadata).filter(Metadata.id == metadato_id).first()
    if db_metadato:
        db.delete(db_metadato)
        db.commit()
    return db_metadato
