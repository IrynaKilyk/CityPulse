CREATE TABLE weather_data(
    id INT GENERATED ALWAYS AS IDENTITY  PRIMARY KEY,
    city_id INT REFERENCES cities(id),
    recorded_at TIMESTAMP,
    temperature FLOAT,
    relative_humidity FLOAT,
    wind_speed FLOAT,
    weather_code INT

)