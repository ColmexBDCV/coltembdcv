from sqlalchemy.orm import Session

from models import Site
from models.default_facet_filter import DefaultFacetFilter
from models.facet_filter_model import FacetFilter
from schemas.facet_filter_schema import FacetFilterCreate


# Crear un nuevo filtro de facetas
def create_facet_filter(db: Session, site_id: int, filter_data: FacetFilterCreate, user_id: int):
    new_filter = FacetFilter(
        site_id=site_id,
        filter_key=filter_data.filter_key,
        active=filter_data.active,
        user_id=user_id
    )
    db.add(new_filter)
    db.commit()
    db.refresh(new_filter)
    return new_filter


# Alternar el estado de activación de un filtro de facetas
def toggle_facet_filter_status(db: Session, filter_id: int, user_id: int):
    filter_item = db.query(FacetFilter).filter(FacetFilter.id == filter_id).first()
    if not filter_item:
        raise ValueError("Filter not found")

    filter_item.active = not filter_item.active
    filter_item.user_id = user_id
    db.commit()
    db.refresh(filter_item)

    return filter_item


# Obtener todos los filtros de facetas para un sitio
def get_facet_filters_for_site(db: Session, site_id: int):
    return db.query(FacetFilter).filter(FacetFilter.site_id == site_id).all()

def create_default_facet_filter(db: Session, filter_key: str, user_id: int):
    # Crear el filtro por defecto
    new_default_filter = DefaultFacetFilter(filter_key=filter_key)
    db.add(new_default_filter)
    db.commit()
    db.refresh(new_default_filter)

    # Relacionar el nuevo filtro con todos los sitios existentes, pero apagado (active=False)
    all_sites = db.query(Site).all()
    for site in all_sites:
        new_filter = FacetFilter(
            site_id=site.id,
            filter_key=filter_key,
            active=False,  # Apagado por defecto
            user_id=user_id
        )
        db.add(new_filter)

    db.commit()
    return new_default_filter