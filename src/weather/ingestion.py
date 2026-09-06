import requests
from pydantic import BaseModel

from ..ingestion_runner import run_ingestion


class WeatherResponse(BaseModel):
    temperature_2m: float
    time: str
    relative_humidity_2m: float 
    wind_speed_10m: float
    weather_code: int

    
def fetch_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude":lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    weather_response = WeatherResponse(**data["current"])


    weather_data = {
    "temperature": weather_response.temperature_2m,
    "time": weather_response.time,
    "relative_humidity": weather_response.relative_humidity_2m,
    "wind_speed": weather_response.wind_speed_10m,
    "weather_code": weather_response.weather_code
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
        
    run_ingestion(fetch_weather,insert_weather_data, "logs/weather.log",'weather')
                
    
if __name__ == "__main__":
    main()    

