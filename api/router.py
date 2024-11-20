from fastapi import APIRouter
from api.v1.endpoints import user_controller, site_controller, \
    field_filter_controller, facet_filter_controller, article_filter_controller, thematic_site_controller, contact_controller

api_router = APIRouter()
api_router.include_router(user_controller.router, prefix="/users", tags=["users"])
api_router.include_router(site_controller.router, prefix="/sites", tags=["sites"])
api_router.include_router(field_filter_controller.router, prefix="/field_filters", tags=["field_filters"])
api_router.include_router(facet_filter_controller.router, prefix="/facet_filters", tags=["facet_filters"])
api_router.include_router(article_filter_controller.router, prefix="/article_filters", tags=["article_filters"])
api_router.include_router(thematic_site_controller.router, prefix="/thematic", tags=["thematic"])
api_router.include_router(contact_controller.router, prefix="/contact", tags=["contact"])