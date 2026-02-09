from database import pool
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Vehicle(BaseModel):
    make: str
    model: str
    year: str
    color: str

class PlateSighting(BaseModel):
    id: str
    longitude: float
    latitude: float
    timestamp: datetime
    vehicle: Optional[Vehicle] = None

class Plate(BaseModel):
    id: str
    code: str
    sightings: list[PlateSighting]


def create_plate(plate_code: str, longitude: float, latitude: float):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT (code, longitude, latitude) VALUES ($1, $2, $3);',
                [ plate_code, longitude, latitude ]
            )

def fetch_plate_by_code(plate_code: str) -> Plate | None:
    plate = None
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT * FROM plate WHERE code = $1 LIMIT 1;;',
                [ plate_code ]
            )

            plate = cur.fetchone()
    return plate