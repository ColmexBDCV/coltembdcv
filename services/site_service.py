from sqlalchemy.orm import Session

from models import FieldFilter, FacetFilter, ArticleFilter
from models.default_article_filter import DefaultArticleFilter
from models.default_facet_filter import DefaultFacetFilter
from models.default_field_filter import DefaultFieldFilter
from models.site_model import Site
from schemas.site_schemas import SiteCreate

# Crear un sitio
def create_site(db: Session, site_data: SiteCreate, user_id: int):
    # Crear el nuevo sitio
    new_site = Site(
        name=site_data.name,
        repository_url=site_data.repository_url,
        base_url=site_data.base_url,
        link_url=site_data.link_url,
        user_id=user_id
    )
    db.add(new_site)
    db.commit()
    db.refresh(new_site)

    # Agregar los filtros por defecto activados al nuevo sitio
    default_field_filters = db.query(DefaultFieldFilter).all()
    for default_filter in default_field_filters:
        new_filter = FieldFilter(
            site_id=new_site.id,
            filter_key=default_filter.filter_key,
            active=True,  # Activado por defecto
            user_id=user_id
        )
        db.add(new_filter)

    default_facet_filters = db.query(DefaultFacetFilter).all()
    for default_filter in default_facet_filters:
        new_filter = FacetFilter(
            site_id=new_site.id,
            filter_key=default_filter.filter_key,
            active=True,  # Activado por defecto
            user_id=user_id
        )
        db.add(new_filter)

    default_article_filters = db.query(DefaultArticleFilter).all()
    for default_filter in default_article_filters:
        new_filter = ArticleFilter(
            site_id=new_site.id,
            filter_key=default_filter.filter_key,
            active=True,  # Activado por defecto
            user_id=user_id
        )
        db.add(new_filter)

    db.commit()
    return new_site


# Obtener un sitio por su ID
def get_site_by_id(db: Session, site_id: int):
    return db.query(Site).filter(Site.id == site_id).first()

# Obtener todos los sitios
def get_all_sites(db: Session):
    return db.query(Site).all()
