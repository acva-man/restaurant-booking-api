from fastapi import FastAPI
from app.routers import tables, reservations
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tables.router)
app.include_router(reservations.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Restaurant Booking API"}
