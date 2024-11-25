from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database.db import get_db
from database import models
from schema.schemas import LogResponse


router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/all", response_model=LogResponse)
async def get_logs(db: Session = Depends(get_db)):
    log_data = db.query(models.Logs)
    if log_data.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "No Log found"},
        )
    log_data = log_data.order_by(models.Logs.created_at.desc()).limit(100).all()
    if log_data:
        return {"status": "ok", "items": log_data}


@router.get("/{endpoint_id}", response_model=LogResponse)
async def get_logs(endpoint_id: int, db: Session = Depends(get_db)):
    log_data = db.query(models.Logs).filter(models.Logs.endpoint_id == endpoint_id)
    if log_data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    log_data = log_data.order_by(models.Logs.created_at.desc()).limit(100).all()
    if log_data:
        return {"status": "ok", "items": log_data}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "No Log found for this endpointID"},
    )
