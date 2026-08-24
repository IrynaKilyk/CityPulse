# CityPulse
a data engineering project for collecting, processing, and analyzing urban from multiple sources

## Current Scope
- Weather data ingestion
- API integration
- Data validation
- CSV storage
- Logging

## Tech stack
- Python
- PostgresSQL
- Docker
- Airflow
- Alembic (database migrations)

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

4. Start the database:
```powershell
   docker-compose up -d
```

5. Apply database migrations:
```powershell
   alembic upgrade head
```

## Database migrations

Schema changes are managed with Alembic, not by editing the `.sql` files directly.

- `database/*.sql` — reference schema (what the DB looks like on a fresh setup)
- `alembic/versions/` — history of schema changes applied over time

To create a new migration after changing the schema:
```powershell
alembic revision -m "short description of the change"
```
Then edit the generated file in `alembic/versions/` and write the change in `upgrade()` (and its reverse in `downgrade()`).

To apply migrations:
```powershell
alembic upgrade head
```

To check the current migration state:
```powershell
alembic current
```