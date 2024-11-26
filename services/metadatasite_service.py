from sqlalchemy.orm import Session, joinedload
from models.metadatasite_model import MetadataSite
from schemas.metadatasite_schema import MetadataSiteCreate, MetadataSiteUpdate

def create_metadata_site(db: Session, metadata_site: MetadataSiteCreate):
    db_metadata_site = MetadataSite(**metadata_site.dict())
    db.add(db_metadata_site)
    db.commit()
    db.refresh(db_metadata_site)
    return db_metadata_site

def get_metadata_sites(db: Session, id_site: int, id_registro: str, skip: int = 0, limit: int = 100):
    return (
        db.query(MetadataSite)
        .options(joinedload(MetadataSite.metadatas))
        .filter(MetadataSite.id_site == id_site, MetadataSite.id_registro == id_registro)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_metadata_site(db: Session, metadata_site_id: int):
    return db.query(MetadataSite).filter(MetadataSite.id == metadata_site_id).first()

def update_metadata_site(db: Session, db_metadata_site: MetadataSite, metadata_site_update: MetadataSiteUpdate):
    for key, value in metadata_site_update.dict(exclude_unset=True).items():
        setattr(db_metadata_site, key, value)
    db.commit()
    db.refresh(db_metadata_site)
    return db_metadata_site

def delete_metadata_site(db: Session, metadata_site_id: int):
    db_metadata_site = db.query(MetadataSite).filter(MetadataSite.id == metadata_site_id).first()
    if db_metadata_site:
        db.delete(db_metadata_site)
        db.commit()
    return db_metadata_site
