from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.table import Table as TableModel
from app.schemas.table import Table as TableSchema, TableCreate
from app.database import get_db

router = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)

@router.post("/", 
             response_model=TableSchema,
             status_code=status.HTTP_201_CREATED)
def create_table(table: TableCreate, 
                db: Session = Depends(get_db)):
    """
    Create a new table in the restaurant
    """
    db_table = TableModel(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.get("/", 
            response_model=List[TableSchema])
def get_tables(skip: int = 0, 
               limit: int = 100,
               db: Session = Depends(get_db)):
    """
    Get list of all tables with pagination
    """
    tables = db.query(TableModel).offset(skip).limit(limit).all()
    return tables

@router.get("/{table_id}", 
            response_model=TableSchema)
def get_table(table_id: int, 
              db: Session = Depends(get_db)):
    """
    Get specific table by ID
    """
    table = db.query(TableModel).filter(TableModel.id == table_id).first()
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with id {table_id} not found"
        )
    return table

@router.delete("/{table_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int,
                 db: Session = Depends(get_db)):
    """
    Delete a table by ID
    """
    table_query = db.query(TableModel).filter(TableModel.id == table_id)
    table = table_query.first()
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with id {table_id} not found"
        )
    
    table_query.delete(synchronize_session=False)
    db.commit()
    return