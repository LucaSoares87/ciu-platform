from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from ..core.database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    state = Column(String(2), nullable=False)

    intersections = relationship("Intersection", back_populates="city")


class Intersection(Base):
    __tablename__ = "intersections"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(String, nullable=True)

    city = relationship("City", back_populates="intersections")
    cameras = relationship("Camera", back_populates="intersection")
    observations = relationship("TrafficObservation", back_populates="intersection")


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    intersection_id = Column(Integer, ForeignKey("intersections.id"), nullable=False)
    name = Column(String, nullable=False)
    rtsp_url = Column(String, nullable=True)
    status = Column(String, default="ACTIVE")

    intersection = relationship("Intersection", back_populates="cameras")
    observations = relationship("TrafficObservation", back_populates="camera")


class TrafficObservation(Base):
    __tablename__ = "traffic_observations"

    id = Column(Integer, primary_key=True, index=True)
    intersection_id = Column(Integer, ForeignKey("intersections.id"), nullable=False)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cars_count = Column(Integer, default=0)
    motorcycles_count = Column(Integer, default=0)
    buses_count = Column(Integer, default=0)
    trucks_count = Column(Integer, default=0)
    bicycles_count = Column(Integer, default=0)
    pedestrians_count = Column(Integer, default=0)
    average_speed = Column(Float, default=0.0)
    queue_length = Column(Integer, default=0)
    congestion_level = Column(Float, default=0.0)

    intersection = relationship("Intersection", back_populates="observations")
    camera = relationship("Camera", back_populates="observations")