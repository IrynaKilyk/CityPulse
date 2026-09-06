import requests
from pydantic import BaseModel

from ..ingestion_runner import run_ingestion


class AirQualityResponse(BaseModel):
    pm10: float
    time: str
    pm2_5: float
    carbon_monoxide: float

def fetch_air_quality(lat:float, lon:float):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "pm10,pm2_5,carbon_monoxide"
    }

    response =  requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    air_quality_response = AirQualityResponse(**data["current"])
    air_quality_data = {
        "pm10": air_quality_response.pm10,
        "pm2_5": air_quality_response.pm2_5,
        "carbon_monoxide": air_quality_response.carbon_monoxide,
        "recorded_at": air_quality_response.time
    }
    return air_quality_data

def insert_air_quality(conn, city_id: int, air_quality_data:dict):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO 
        air_quality(city_id, recorded_at, pm10, pm2_5, carbon_monoxide)
        VALUES(%s, %s, %s, %s, %s)""",(
            city_id,
            air_quality_data['recorded_at'],
            air_quality_data['pm10'],
            air_quality_data['pm2_5'],
            air_quality_data['carbon_monoxide'])
            )
        conn.commit()



def main():

    run_ingestion(fetch_air_quality, insert_air_quality, 'logs/air_quality.log', 'air quality')
    
if __name__ == "__main__":
    main()    