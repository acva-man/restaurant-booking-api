from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    reservation_time = Column(DateTime(timezone=True), server_default=func.now())
    duration_minutes = Column(Integer)
