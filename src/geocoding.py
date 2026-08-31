import requests
import logging


def get_coordinates(city_name: str, target_region:str, target_country:str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 10,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    if "results" not in data:
        logging.warning(f"City '{city_name}' not found in API")
        return None
    
    for item in data["results"]:
        api_country = item.get("country")
        api_region = item.get("admin1")

        if api_country == target_country and api_region == target_region:
            lat = item["latitude"]
            lon = item["longitude"]
            country = item["country"]
            region = item["admin1"]

            geocoding_result ={
                "lat": lat,
                "lon": lon,
                "country": country,
                "region": region
            }
            return geocoding_result
        
    logging.warning(f"City '{city_name} found, but not in {target_country} or {target_region}")
    return None

