from sqlalchemy.orm import Session

from models import Site
from models.default_field_filter import DefaultFieldFilter
from models.field_filter_model import FieldFilter
from schemas.field_filter_schema import FieldFilterCreate


# Crear un nuevo filtro de campos
def create_field_filter(db: Session, site_id: int, filter_data: FieldFilterCreate, user_id: int):
    new_filter = FieldFilter(
        site_id=site_id,
        filter_key=filter_data.filter_key,
        active=filter_data.active,
        user_id=user_id
    )
    db.add(new_filter)
    db.commit()
    db.refresh(new_filter)
    return new_filter


# Alternar el estado de activación de un filtro
def toggle_filter_status(db: Session, filter_id: int, user_id: int):
    filter_item = db.query(FieldFilter).filter(FieldFilter.id == filter_id).first()
    if not filter_item:
        raise ValueError("Filter not found")

    # Alternar el estado del filtro
    filter_item.active = not filter_item.active
    filter_item.user_id = user_id
    db.commit()
    db.refresh(filter_item)

    return filter_item


# Obtener todos los filtros de campos para un sitio
def get_field_filters_for_site(db: Session, site_id: int):
    return db.query(FieldFilter).filter(FieldFilter.site_id == site_id).all()

def create_default_field_filter(db: Session, filter_key: str, user_id: int, iterable: bool):
    # Crear el filtro por defecto
    new_default_filter = DefaultFieldFilter(filter_key=filter_key)
    db.add(new_default_filter)
    db.commit()
    db.refresh(new_default_filter)

    # Relacionar el nuevo filtro con todos los sitios existentes, pero apagado (active=False)
    all_sites = db.query(Site).all()
    for site in all_sites:
        new_filter = FieldFilter(
            site_id=site.id,
            iterable= iterable,
            filter_key=filter_key,
            active=False,  # Apagado por defecto
            user_id=user_id
        )
        db.add(new_filter)

    db.commit()
    return new_default_filter
