import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.session import get_db
from models import Site, FieldFilter, FacetFilter, ArticleFilter, DocumentType
from schemas.document_data_request import DocumentDataRequest
from schemas.facet_filter_request_schema import FilterRequest
from schemas.modal_facet_schema import ModalFacetRequest
from schemas.contact_request_schema import ContactRequest
from services.map_service import build_url_with_filters
from services.thematic_service import get_document_data_service, build_facet_url, fetch_facet_data, is_next_page, send_message_to_teams
from utils.filter_logic import filter_data

router = APIRouter()

@router.post("/{site_id}/message/")
async def contact_teams(site_id: int, request: ContactRequest, db: Session = Depends(get_db)):
    # Obtener el nombre del sitio desde la base de datos
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Sitio no encontrado")

    # Crear el título del mensaje para Teams
    title = f"Contacto desde {site.name}"

    # Enviar el mensaje a Teams
    success = send_message_to_teams(
        title=title,
        mail=request.mail,
        asunto=request.asunto,
        mensaje=request.mensaje,
        webhook_url=site.contacto_webhook
    )

    if not success:
        raise HTTPException(status_code=500, detail="Error al enviar el mensaje a Teams")
    return {"message": "Mensaje enviado a Teams con éxito"}