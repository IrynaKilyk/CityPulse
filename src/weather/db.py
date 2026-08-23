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
  