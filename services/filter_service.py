from sqlalchemy.orm import Session
from models.field_filter_model import FieldFilter
from models.facet_filter_model import FacetFilter
from models.article_filter_model import ArticleFilter

def get_field_filters(db: Session, site_id: int):
    return db.query(FieldFilter).filter(FieldFilter.site_id == site_id, FieldFilter.active == 1).all()

def get_facet_filters(db: Session, site_id: int):
    return db.query(FacetFilter).filter(FacetFilter.site_id == site_id, FacetFilter.active == 1).all()

def get_article_filters(db: Session, site_id: int):
    return db.query(ArticleFilter).filter(ArticleFilter.site_id == site_id, ArticleFilter.active == 1).all()
