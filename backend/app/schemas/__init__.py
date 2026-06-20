from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CityBase(BaseModel):
    name: str
    state: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class IntersectionBase(BaseModel):
    name: str
    latitude: Optional[float] = Field(None, description="Latitude do cruzamento")
    longitude: Optional[float] = Field(None, description="Longitude do cruzamento")
    description: Optional[str] = None


class IntersectionCreate(IntersectionBase):
    city_id: int


class Intersection(IntersectionBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True


class CameraBase(BaseModel):
    name: str
    rtsp_url: Optional[str] = None
    status: Optional[str] = "ACTIVE"


class CameraCreate(CameraBase):
    intersection_id: int


class Camera(CameraBase):
    id: int
    intersection_id: int

    class Config:
        orm_mode = True


class TrafficObservationBase(BaseModel):
    cars_count: int = 0
    motorcycles_count: int = 0
    buses_count: int = 0
    trucks_count: int = 0
    bicycles_count: int = 0
    pedestrians_count: int = 0
    average_speed: float = 0.0
    queue_length: int = 0
    congestion_level: float = 0.0


class TrafficObservationCreate(TrafficObservationBase):
    intersection_id: int
    camera_id: int


class TrafficObservation(TrafficObservationBase):
    id: int
    intersection_id: int
    camera_id: int
    timestamp: datetime

    class Config:
        orm_mode = True