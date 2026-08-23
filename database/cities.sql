CREATE TABLE cities(
     id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
     city_name VARCHAR(255),
     latitude FLOAT,
     longitude FLOAT

)