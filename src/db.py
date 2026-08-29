import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            gssencmode="disable"
        )
        return conn

def get_or_create_city(conn, city_name: str, lat: float, lon: float, country: str, region: str):
    with conn.cursor() as cur:
        cur.execute("""
    INSERT INTO cities(city_name, latitude, longitude, country, region) 
    VALUES(%s, %s, %s, %s, %s)
    ON CONFLICT (city_name) DO NOTHING;""",
        (city_name, lat, lon , country, region)
    )
    conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT id from cities WHERE city_name = %s", (city_name,))
        number_id =cur.fetchone()[0]
    return number_id
  