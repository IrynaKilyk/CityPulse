import sys
import logging
from db import get_connection, get_or_create_city
from geocoding import get_coordinates
from config import TARGET_LOCATIONS


def run_ingestion(fetch_fn, insert_fn, log_filename, source_name):
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
        )
            
    conn = get_connection()
    logging.info("Connecting successfully")
            
    try:
        for data in TARGET_LOCATIONS:
            cords_data = get_coordinates(data["city"], data["region"], data["country"])
            if not cords_data:
                continue
                
            data_item = fetch_fn(cords_data["lat"], cords_data["lon"])
            city_id = get_or_create_city(conn, data["city"], cords_data["lat"], cords_data["lon"], data["country"], data["region"])
            insert_fn(conn, city_id, data_item)
            logging.info(f"[{source_name}] Information about city {data['city']} successfully saved!")
                    
    except Exception as e:
        logging.error(f'error: {e}')
        conn.rollback()
        sys.exit(1)
                    
    finally:
        conn.close()
        logging.info('Connection with bd closed!')