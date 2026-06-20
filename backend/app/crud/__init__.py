from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas


def get_cities(db: Session) -> List[models.City]:
    return db.query(models.City).all()


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_intersections(db: Session, city_id: Optional[int] = None) -> List[models.Intersection]:
    query = db.query(models.Intersection)
    if city_id:
        query = query.filter(models.Intersection.city_id == city_id)
    return query.all()


def create_intersection(db: Session, intersection: schemas.IntersectionCreate) -> models.Intersection:
    db_intersection = models.Intersection(**intersection.dict())
    db.add(db_intersection)
    db.commit()
    db.refresh(db_intersection)
    return db_intersection


def get_cameras(db: Session, intersection_id: Optional[int] = None) -> List[models.Camera]:
    query = db.query(models.Camera)
    if intersection_id:
        query = query.filter(models.Camera.intersection_id == intersection_id)
    return query.all()


def create_camera(db: Session, camera: schemas.CameraCreate) -> models.Camera:
    db_camera = models.Camera(**camera.dict())
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera


def create_observation(db: Session, observation: schemas.TrafficObservationCreate) -> models.TrafficObservation:
    db_obs = models.TrafficObservation(**observation.dict())
    db.add(db_obs)
    db.commit()
    db.refresh(db_obs)
    return db_obs


def get_observations(db: Session, intersection_id: Optional[int] = None) -> List[models.TrafficObservation]:
    query = db.query(models.TrafficObservation)
    if intersection_id:
        query = query.filter(models.TrafficObservation.intersection_id == intersection_id)
    return query.all()