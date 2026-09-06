# CityPulse
## A data engineering project for collecting, processing, and analyzing urban data (weather, air quality, and traffic) from multiple external sources.

## Current Scope
- Weather data ingestion (Open-Meteo)
- Air quality data ingestion (Open-Meteo Air Quality API)
- Traffic data ingestion (TomTom Traffic API)
- Geocoding (city name → coordinates), with country/region matching
- API response validation with Pydantic
- Logging per data source
- Schema management via Alembic migrations

## Tech stack
- Python
- PostgresSQL
- Docker / Docker Compose
- Alembic (database migrations)
- Pydantic (data validation)
- Ruff (linting and formatting)
- Airflow (planned — not yet integrated)

## Setup

1. Create and activate a virtual environment:
```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
   pip install -r requirements.txt
```

3. Copy `.dist.env` to `.env` and fill in your local database credentials.
Start the database:
   docker-compose up -d
Apply database migrations:
   alembic upgrade head

## Database migrations

Schema changes are managed with Alembic — it is the single source of truth for the database schema.

- `alembic/versions/` — full history of schema changes

To create a new migration after changing the schema:

```powershell
alembic revision -m "short description of the change"
```
To apply migrations:

```powershell
alembic upgrade head
```

To check the current migration state:

```powershell
alembic current
```

## Linting

This project uses Ruff for linting and import sorting.

```powershell
ruff check src/
ruff check --fix src/
```

Line endings are normalized to LF via `.gitattributes`.
