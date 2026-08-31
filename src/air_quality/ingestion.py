import requests
import sys
import os
import logging

logging.basicConfig(
    filename="logs/air_quality.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # reminder to fix it

from geocoding import get_coordinates
from db import get_connection, get_or_create_city
from config import TARGET_LOCATIONS

def fetch_air_quality(lat:float, lon:float):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "pm10,pm2_5,carbon_monoxide"
    }

    response =  requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    pm10 = data["current"]["pm10"]
    time = data["current"]['time']
    pm2_5 = data["current"]["pm2_5"]
    carbon_monoxide = data["current"]["carbon_monoxide"]

    air_quality_data = {
        "pm10": pm10,
        "pm2_5": pm2_5,
        "carbon_monoxide": carbon_monoxide,
        "recorded_at": time
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
    conn = get_connection()
    logging.info("Connecting successfully")

 
    try:
        for data in TARGET_LOCATIONS:
            cords_data = get_coordinates(data["city"], data["region"], data["country"])
            if not cords_data:
                continue

            city_name = data["city"]
            country = data["country"]
            region = data["region"]
            lat = cords_data["lat"]
            lon = cords_data["lon"]

            air_quality_data = fetch_air_quality(cords_data["lat"], cords_data["lon"])
            city_id = get_or_create_city(conn, city_name, lat, lon, country, region)
            insert_air_quality(conn, city_id, air_quality_data)
            logging.info(f"Information about city {city_name} successfully saved!")

    except Exception  as e:
        logging.error(f"Error {e}")
        conn.rollback()
        sys.exit(1)

    finally:
        conn.close()
        logging.info("Connection with bd closed!")

    
if __name__ == "__main__":
    main()    