from sqlalchemy.orm import joinedload
from collections import defaultdict
from models.metadatasite_model import MetadataSite

def remove_solr_sufix(key):
    key = key.replace("_tesim", "")
    key = key.replace("_ssim", "")
    key = key.replace(" Sim", "")
    key = key.replace("_sim", "")
    return key


def filter_data(data, field_filters, facet_filters, article_filters):
    # Convertimos los filtros en sets para realizar la comparación correctamente
    field_filter_keys = {remove_solr_sufix(f.filter_key) for f in field_filters}
    facet_filter_keys = {remove_solr_sufix(f.filter_key) for f in facet_filters}
    iterable_field_filter_keys = {remove_solr_sufix(f.filter_key) for f in field_filters if f.iterable}
    # Verificar si "response" está en los datos y luego "docs" dentro de response
    if "response" in data and "docs" in data["response"]:
        docs = data["response"]["docs"]
        for doc in docs:
            iterables = {}
            keys = list(doc.keys())
            for key in keys:
                new_key = remove_solr_sufix(key)
                if new_key in field_filter_keys:
                    # Si es iterable lo movemos a la nueva clave 'iterables'
                    if new_key in iterable_field_filter_keys:
                        iterables[new_key] = doc.pop(key)
                    else:
                        doc[new_key] = doc.pop(key)
                else:
                    doc.pop(key, None)
            if iterables:
                doc['iterables'] = iterables

        new_facets = []
        if "facets" in data["response"]:
            for facet in data["response"]["facets"]:
                df = remove_solr_sufix(facet["label"])
                if df in facet_filter_keys:
                    if facet.get("items"):
                        facet["label"] = df
                        new_facets.append(facet)

        data["response"]["facets"] = new_facets

    return data

def filter_article_data(data, article_filters, db_session):
    from sqlalchemy.orm.exc import NoResultFound
    from sqlalchemy.exc import SQLAlchemyError
    from collections import defaultdict

    article_filter_keys = {remove_solr_sufix(f.filter_key) for f in article_filters}
    iterable_article_filter_keys = {remove_solr_sufix(f.filter_key) for f in article_filters if f.iterable}

    filtered_data = {}
    iterables = defaultdict(list)

    try:
        for key, value in data.items():
            new_key = remove_solr_sufix(key)

            if new_key in article_filter_keys and value not in [None, "", [], {}]:
                if new_key in iterable_article_filter_keys:
                    iterables[new_key] = value
                else:
                    filtered_data[new_key] = value

            if key == "id" and isinstance(value, dict) and "id" in value:
                id_registro = value["id"]

                if not id_registro:
                    continue

                try:
                    related_metadata = (
                        db_session.query(MetadataSite)
                        .options(joinedload(MetadataSite.metadatas))
                        .filter(MetadataSite.id_registro == id_registro)
                        .all()
                    )

                    for metadata in related_metadata:
                        iterables[metadata.metadatas.nombre].append(metadata.valor)

                except NoResultFound:
                    print(f"No se encontraron datos para id_registro: {id_registro}")
                except SQLAlchemyError as e:
                    print(f"Error de SQLAlchemy: {e}")

        if iterables:
            filtered_data["iterables"] = dict(iterables)

        return filtered_data

    except Exception as e:
        print(f"Error al filtrar los datos: {e}")
        raise


