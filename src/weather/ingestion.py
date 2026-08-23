import os
import requests
from db import get_connection

conn = get_connection()
print("Connecting successfully:", conn)

url = "https://api.open-meteo.com/v1/forecast"

params = {
        "latitude": 49.84,
        "longitude": 24.03,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
}

response = requests.get(url, params=params)

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
cur = conn.cursor()
cur.execute("INSERT INTO cities(city_name, latitude, longitude) VALUES(%s, %s, %s)",
    ("Lviv", params["latitude"],params["longitude"] )
)
conn.commit()

cur = conn.cursor()
cur.execute("INSERT INTO weather_data (city_id, recorded_at, temperature, relative_humidity, wind_speed, weather_code ) VALUES (%s, %s, %s, %s, %s, %s)",
    (1, weather_data["time"], weather_data["temperature"], weather_data["relative_humidity"], weather_data["wind_speed"], weather_data["weather_code"])
)
conn.commit()

