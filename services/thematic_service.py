import requests
from sqlalchemy.orm import Session

from models import FieldFilter, FacetFilter, ArticleFilter
from models.site_model import Site
from models.document_type_model import DocumentType
from utils.filter_logic import filter_data, filter_article_data


def get_document_data_service(db: Session, site_id: int, document_data: dict):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise ValueError("Site not found")

    base_url = site.base_url
    document_type = db.query(DocumentType).filter(
        DocumentType.type_name == document_data['has_model'], DocumentType.activo == True
    ).first()

    if not document_type:
        raise ValueError("Document type not active or not found")

    full_url = f"{base_url}concern/{document_type.type}/{document_data['id']}.json"

    response = requests.get(full_url)
    response_data = response.json()

    # Lógica adicional de filtrado
    filtered_data = filter_article_data(
        response_data,
        article_filters=db.query(ArticleFilter).filter(ArticleFilter.site_id == site_id,
                                                                                ArticleFilter.active == True).all(),
        db_session=db
    )

    return {"site": site, "data": filtered_data}


def build_facet_url(site, facet_label, facet_sort, facet_page, filters, search):
    # Construimos la base URL desde el sitio
    base_url = f"{site.base_url}/catalog/facet/{facet_label}.json?search_field=all_fields&q={search or ''}"

    # Agregar cada filtro con su clave y valor a la URL
    for facet in filters:
        base_url += f"&f[{facet.key}][]={facet.value}"

    # Agregar parámetros de la faceta
    base_url += f"&facet.page={facet_page}&facet.sort={facet_sort}&locale=es"

    # Agregar la URL param del sitio
    if site.repository_url:
        base_url += f"&{(site.repository_url).split('?')[1]}"

    return base_url


def fetch_facet_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching facet data: {e}")
        return None

def is_next_page(site, facet_label, facet_sort, facet_page, filters, search):
    next_facet_page = facet_page + 1
    url = build_facet_url(site, facet_label, facet_sort, next_facet_page, filters, search)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if(data["response"]["facets"]["items"]):
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error fetching facet data: {e}")


def send_message_to_teams(title: str, mail: str, asunto: str, mensaje: str, webhook_url: str) -> bool:
    #webhook_url = "https://redescolmex.webhook.office.com/webhookb2/f5f44f0f-371e-4c95-b39d-4da3e230bb4e@93db1ea2-0b31-43e8-aece-2228fabb7af1/IncomingWebhook/8bbfaaeaaee34e458e2e0510acf92eef/811356f3-d509-4767-9780-a7bf281c13b6/V2Reivy6bmOBZ1Fd26f4G3MUZqcdi6ieE3EYHYfS4IXW41"

    # Crear el payload para Teams
    payload = {
        "title": title,
        "text": (f"**Correo**: {mail}\n\n"
            f"**Asunto**: {asunto}\n\n"
            f"**Mensaje**:\n{mensaje}"
            )
    }

    try:
        # Enviar la solicitud a Teams
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Lanza un error si la solicitud falla
        return True
    except requests.RequestException as e:
        print(f"Error al enviar mensaje a Teams: {e}")
        return False