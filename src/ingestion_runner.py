import logging
import sys

from .config import TARGET_LOCATIONS
from .db import get_connection, get_or_create_city
from .geocoding import get_coordinates

logger = logging.getLogger(__name__)

def run_ingestion(fetch_fn, insert_fn, log_filename, source_name):
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
        )
            
    conn = get_connection()
    logger.info("Connecting successfully")
            
    try:
        for data in TARGET_LOCATIONS:
            cords_data = get_coordinates(data["city"], data["region"], data["country"])
            if not cords_data:
                continue
                
            data_item = fetch_fn(cords_data["lat"], cords_data["lon"])
            city_id = get_or_create_city(conn, data["city"], cords_data["lat"], cords_data["lon"], data["country"], data["region"])
            insert_fn(conn, city_id, data_item)
            logger.info(f"[{source_name}] Information about city {data['city']} successfully saved!")
                    
    except Exception as e: # noqa: BLE001
        logger.error(f'error: {e}')
        conn.rollback()
        sys.exit(1)
                    
    finally:
        conn.close()
        logger.info('Connection with bd closed!')