from sqlalchemy.ext.declarative import declarative_base

# Crear la base común de la que todos los modelos heredarán
Base = declarative_base()

# Importa todos los modelos explícitamente para que Alembic los detecte
from models.user_auth_model import UserAuth
from models.user_info_model import UserInfo
from models.site_model import Site
from models.field_filter_model import FieldFilter
from models.facet_filter_model import FacetFilter
from models.article_filter_model import ArticleFilter
from models.default_field_filter import DefaultFieldFilter
from models.default_facet_filter import DefaultFacetFilter
from models.default_article_filter import DefaultArticleFilter
from models.document_type_model import DocumentType
from models.map_model import Map
from models.map_filter_model import MapFilter
from models.default_map_filter_model import DefaultMapFilter
from models.metadata_model import Metadata
from models.metadatasite_model import MetadataSite