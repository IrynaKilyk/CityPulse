import requests
import json
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import get_connection

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


def main():
    conn = get_connection()
    print("Connecting successfully:", conn)

    with open('data/cities.json', 'r', encoding='utf-8') as f:
        my_data_list =json.load(f)
    try:
        for data in my_data_list:
            city_name = data["name"]
            lat = data["lat"]
            lon = data["lon"]

            air_quality_data = fetch_air_quality(lat, lon)
            city_id = get_or_create_city(conn, city_name, lat, lon)
            insert_air_quality(conn, city_id, air_quality_data)

    except Exception  as e:
        print(f'Error {e}')
        conn.rollback()

    finally:
        conn.close()
        print('Connection with bd closed!')

    
if __name__ == "__main__":
    main()    