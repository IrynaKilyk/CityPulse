import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

from ..ingestion_runner import run_ingestion


class TrafficResponse(BaseModel):
    currentSpeed: int
    freeFlowSpeed: int
    currentTravelTime: int
    freeFlowTravelTime: int
    roadClosure: bool
    

load_dotenv()

api_key = os.getenv("TOMTOM_API_KEY")
if not api_key:
    raise ValueError("TOMTOM_API_KEY is not set")

api_key = api_key.strip()

def fetch_traffic_data(lat:float, lon:float):

    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}"

    params = {
        "key": api_key,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    segment_data = data["flowSegmentData"]

    traffic_response = TrafficResponse(**segment_data)

    traffic_data ={
       "recorded_at": datetime.now(tz=timezone.utc),
        "current_speed": traffic_response.currentSpeed,
        "free_flow_speed": traffic_response.freeFlowSpeed,
        "current_travel_time": traffic_response.currentTravelTime,
        "free_flow_travel_time": traffic_response.freeFlowTravelTime,
        "road_closure": traffic_response.roadClosure
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

    run_ingestion(fetch_traffic_data, insert_traffic_data,'logs/traffic.log', "traffic" )

    
if __name__ == "__main__":
    main()    