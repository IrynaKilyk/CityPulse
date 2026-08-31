import requests
import sys
import os
import logging

logging.basicConfig(
     filename="logs/weather.log",
     level=logging.INFO,
     format="%(asctime)s - %(levelname)s - %(message)s"
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))# reminder to fix it

from db import get_connection, get_or_create_city
from geocoding import get_coordinates
from config import TARGET_LOCATIONS


def fetch_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude":lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    temperature = data["current"]["temperature_2m"] 
    time = data["current"]["time"]
    relative_humidity = data["current"]["relative_humidity_2m"]
    wind_speed = data["current"]["wind_speed_10m"]
    weather_code = data["current"]["weather_code"]

    weather_data = {
    "temperature": temperature,
    "time": time,
    "relative_humidity": relative_humidity,
    "wind_speed": wind_speed,
    "weather_code": weather_code
    }
    return weather_data



def insert_weather_data(conn, city_id: int, weather_data: dict):
    with conn.cursor() as cur:
        cur.execute("""
    INSERT INTO 
    weather_data (city_id, recorded_at, temperature, relative_humidity, wind_speed, weather_code )
    VALUES (%s, %s, %s, %s, %s, %s)""",
        (city_id,
        weather_data["time"],
        weather_data["temperature"],
        weather_data["relative_humidity"],
        weather_data["wind_speed"],
        weather_data["weather_code"])
    )
    conn.commit()

def main():
        
        conn = get_connection()
        logging.info(f"Connecting successfully")
        
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
            
                weather_data = fetch_weather(cords_data["lat"], cords_data["lon"])
                city_id = get_or_create_city(conn, city_name, lat, lon, country, region)
                insert_weather_data(conn, city_id, weather_data)
                logging.info(f"Information about city {city_name} successfully saved!")
                
        except Exception as e:
                logging.error(f'error: {e}')
                conn.rollback()
                sys.exit(1)
                
        finally:
                conn.close()
                logging.info('Connection with bd closed!')
                
    
if __name__ == "__main__":
    main()    

