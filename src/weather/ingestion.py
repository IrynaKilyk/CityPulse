import requests
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import get_connection


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

def get_or_create_city(conn, city_name: str, lat: float, lon: float):
    with conn.cursor() as cur:
        cur.execute("""
    INSERT INTO cities(city_name, latitude, longitude) 
    VALUES(%s, %s, %s)
    ON CONFLICT (city_name) DO NOTHING;""",
        (city_name, lat, lon )
    )
    conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT id from cities WHERE city_name = %s", (city_name,))
        number_id =cur.fetchone()[0]
    return number_id


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
        print("Connecting successfully:", conn)
        
        with open("data/cities.json", "r", encoding="utf-8") as f:
            my_data_list = json.load(f)
        try:
            for data in my_data_list:

                city_name = data["name"]
                lat = data["lat"]
                lon = data["lon"]

                weather_data = fetch_weather(lat, lon)
                city_id = get_or_create_city(conn, city_name, lat, lon)
                insert_weather_data(conn, city_id, weather_data)
                print(f'Information about city {city_name} successfully saved!')
                
        except Exception as e:
                print(f'error: {e}')
                conn.rollback()
                
        finally:
                conn.close()
                print('Connection with bd closed!')
                
    
if __name__ == "__main__":
    main()    

