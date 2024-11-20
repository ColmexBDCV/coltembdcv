import requests
from fastapi import HTTPException

from models import Map, MapFilter, DefaultMapFilter, Site
from sqlalchemy.orm import Session


def build_url_with_filters(db: Session, site_id: int):
    # Obtener el sitio
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise ValueError("Site not found")

    # Obtener los mapas y filtros
    maps = db.query(Map).filter(Map.site_id == site_id, Map.active == True).all()
    map_filters = db.query(MapFilter).filter(MapFilter.site_id == site_id, MapFilter.active == True).all()

    # Crear la cadena de filtros
    str_filters = ""
    for map_filter in map_filters:
        default_filter = db.query(DefaultMapFilter).filter(
            DefaultMapFilter.id == map_filter.id_filter_map_default).first()
        if default_filter:
            str_filters += f"{default_filter.filter_key},"

    # Crear la URL para cada mapa
    urls = []
    for map_ in maps:
        url = f"{site.base_url}all_coordinates?query={map_.facet}:\"{map_.facet_value}\"&fields={str_filters.rstrip(',')}"
        urls.append(url)

    try:
        response = requests.get(urls[0])
        data = response.json()  # Asume que la respuesta es JSON

        organized_data = {
            "years": [],  # Lista de años únicos
            "data_by_year": {}
        }

        for item in data:
            # Obtener el año del campo `date_created_tesim`
            date_created_list = item.get("date_created_tesim", [])
            if date_created_list:
                year = int(date_created_list[0])  # Convertir el año a entero para usarlo como clave
                year_key = f"year_{year}"

                # Añadir el año a la lista de años únicos si no está ya presente
                if year not in organized_data["years"]:
                    organized_data["years"].append(year)

                # Asegurar que existe una lista para el año actual en `data_by_year`
                if year_key not in organized_data["data_by_year"]:
                    organized_data["data_by_year"][year_key] = []

                # Procesar las coordenadas y organizarlas en el formato adecuado
                coordinates = []
                for coord_str in item.get("based_near_coordinates_tesim", []):
                    lat, lng = coord_str.split("|")
                    coordinates.append({"lat": float(lat), "lng": float(lng)})

                # Agregar el item procesado al año correspondiente
                organized_data["data_by_year"][year_key].append({
                    "id": item["id"],
                    "title_tesim": item.get("title_tesim", [])[0] if item.get("title_tesim") else "",
                    "coordinates": coordinates,
                    "thumbnail_path_ss": item.get("thumbnail_path_ss", ""),
                    "based_near_label_tesim": item.get("based_near_label_tesim", []),
                    "has_model_ssim": item.get("has_model_ssim", []),
                    "hasRelatedMediaFragment_ssim": item.get("hasRelatedMediaFragment_ssim", []),
                    "based_near_tesim": item.get("based_near_tesim", []),
                    "date_created_tesim": item.get("date_created_tesim")
                })

        # Ordenar los años para asegurarnos de que `years` esté en orden
        organized_data["years"].sort()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching map coords from repository: {str(e)}")
    return {"site": site, "data": organized_data}
