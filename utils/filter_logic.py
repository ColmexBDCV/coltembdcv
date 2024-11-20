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


def filter_article_data(data, article_filters):
    # Configurar filtros de `article_filter`
    article_filter_keys = {remove_solr_sufix(f.filter_key) for f in article_filters}
    iterable_article_filter_keys = {remove_solr_sufix(f.filter_key) for f in article_filters if f.iterable}

    # Iterar sobre la clave principal de `data` para aplicar los filtros
    filtered_data = {}
    iterables = {}

    for key, value in data.items():
        new_key = remove_solr_sufix(key)
        # Filtrar si `new_key` está en `article_filter_keys`
        if new_key in article_filter_keys and value not in [None, "", [], {}]:
            if new_key in iterable_article_filter_keys:
                iterables[new_key] = value  # Filtrar en `iterables` si es iterable
            else:
                filtered_data[new_key] = value  # Filtrar en `filtered_data` si no es iterable

    # Incluir `iterables` en `filtered_data` si tiene contenido
    if iterables:
        filtered_data['iterables'] = iterables

    return filtered_data