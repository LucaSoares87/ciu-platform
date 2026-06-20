from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ...core.database import get_db
from ... import schemas
from ... import crud


router = APIRouter()


@router.get("/cities", response_model=List[schemas.City])
def read_cities(db: Session = Depends(get_db)):
    """Retorna todas as cidades cadastradas."""
    return crud.get_cities(db)


@router.post("/cities", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)


@router.get("/intersections", response_model=List[schemas.Intersection])
def read_intersections(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Retorna todos os cruzamentos, filtrando opcionalmente por cidade."""
    return crud.get_intersections(db, city_id=city_id)


@router.post("/intersections", response_model=schemas.Intersection, status_code=status.HTTP_201_CREATED)
def create_intersection(intersection: schemas.IntersectionCreate, db: Session = Depends(get_db)):
    return crud.create_intersection(db, intersection)


@router.get("/cameras", response_model=List[schemas.Camera])
def read_cameras(intersection_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_cameras(db, intersection_id=intersection_id)


@router.post("/cameras", response_model=schemas.Camera, status_code=status.HTTP_201_CREATED)
def create_camera(camera: schemas.CameraCreate, db: Session = Depends(get_db)):
    return crud.create_camera(db, camera)


@router.get("/observations", response_model=List[schemas.TrafficObservation])
def read_observations(intersection_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_observations(db, intersection_id=intersection_id)


@router.post("/observations", response_model=schemas.TrafficObservation, status_code=status.HTTP_201_CREATED)
def create_observation(observation: schemas.TrafficObservationCreate, db: Session = Depends(get_db)):
    return crud.create_observation(db, observation)