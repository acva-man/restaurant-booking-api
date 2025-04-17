from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)

def check_table_availability(db: Session, 
                            table_id: int, 
                            reservation_time: datetime, 
                            duration_minutes: int):
    """
    Check if table is available for booking at requested time
    """
    existing = db.query(models.Reservation).filter(
        models.Reservation.table_id == table_id,
        models.Reservation.reservation_time <= reservation_time + timedelta(minutes=duration_minutes),
        models.Reservation.reservation_time + timedelta(
            minutes=models.Reservation.duration_minutes) >= reservation_time
    ).first()
    return existing is None

@router.post("/",
             response_model=schemas.Reservation,
             status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: schemas.ReservationCreate,
                       db: Session = Depends(get_db)):
    """
    Create new reservation with availability check
    """
    # Check if table exists
    table = db.query(models.Table).filter(models.Table.id == reservation.table_id).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with id {reservation.table_id} not found"
        )
    
    # Check availability
    if not check_table_availability(db, 
                                  reservation.table_id, 
                                  reservation.reservation_time, 
                                  reservation.duration_minutes):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Table is already booked for this time slot"
        )
    
    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.get("/",
            response_model=List[schemas.Reservation])
def get_reservations(skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_db)):
    """
    Get list of all reservations with pagination
    """
    reservations = db.query(models.Reservation).offset(skip).limit(limit).all()
    return reservations

@router.get("/{reservation_id}",
            response_model=schemas.Reservation)
def get_reservation(reservation_id: int,
                    db: Session = Depends(get_db)):
    """
    Get specific reservation by ID
    """
    reservation = db.query(models.Reservation).filter(
        models.Reservation.id == reservation_id).first()
    
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with id {reservation_id} not found"
        )
    return reservation

@router.delete("/{reservation_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int,
                       db: Session = Depends(get_db)):
    """
    Delete reservation by ID
    """
    reservation_query = db.query(models.Reservation).filter(
        models.Reservation.id == reservation_id)
    reservation = reservation_query.first()
    
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with id {reservation_id} not found"
        )
    
    reservation_query.delete(synchronize_session=False)
    db.commit()
    return