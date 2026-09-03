import requests
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

api_key = os.getenv("TOMTOM_API_KEY")
if not api_key:
    raise ValueError("TOMTOM_API_KEY is not set")

api_key = api_key.strip()


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # reminder to fix it
from ingestion_runner import run_ingestion


def fetch_traffic_data(lat:float, lon:float):

    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}"

    params = {
        "key": api_key,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    segment_data = data["flowSegmentData"]

    traffic_data ={
       "recorded_at": datetime.now(),
        "current_speed": segment_data['currentSpeed'],
        "free_flow_speed": segment_data['freeFlowSpeed'],
        "current_travel_time": segment_data['currentTravelTime'],
        "free_flow_travel_time": segment_data['freeFlowTravelTime'],
        "road_closure": segment_data['roadClosure']
    }

    return traffic_data

def insert_traffic_data(conn, city_id: int, traffic_data:dict):
    with conn.cursor() as cur:
        cur.execute(""" INSERT INTO traffic_data
         (city_id, recorded_at, current_speed, free_flow_speed, current_travel_time, free_flow_travel_time, road_closure)
           VALUES(%s, %s, %s, %s, %s, %s, %s)""",
           (city_id,
           traffic_data['recorded_at'],
           traffic_data['current_speed'],
           traffic_data['free_flow_speed'],
           traffic_data['current_travel_time'],
           traffic_data['free_flow_travel_time'],
           traffic_data['road_closure']
           )
        )
        
        conn.commit()

def main():

    run_ingestion(fetch_traffic_data, insert_traffic_data,'logs/traffic.log', "Traffic" )

    
if __name__ == "__main__":
    main()    