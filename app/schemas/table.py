from pydantic import BaseModel
from datetime import datetime

class TableBase(BaseModel):
    name: str
    seats: int
    location: str

class TableCreate(TableBase):
    pass

class Table(TableBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Ранее orm_mode в Pydantic v2
