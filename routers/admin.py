from fastapi import status, HTTPException, Depends, APIRouter, Request
from schema.schemas import (
    AddEndpointResponse,
    AddEndpoint,
    AllEndpointResponse,
)
from sqlalchemy.orm import Session
from database.db import get_db
from database import models
from utils import utils


router = APIRouter(prefix="/admin/endpoint", tags=["Manage Endpoints"])


@router.get("/all", response_model=AllEndpointResponse)
async def get_endpoints(request: Request, db: Session = Depends(get_db)):
    endpoints = db.query(models.Endpoints).all()
    return {"status": "ok", "endpoints": endpoints}


@router.post(
    "/add", status_code=status.HTTP_201_CREATED, response_model=AddEndpointResponse
)
async def add_endpoint(
    request: Request, data: AddEndpoint, db: Session = Depends(get_db)
):
    endpoint_data = data.model_dump()
    endpoint = (
        db.query(models.Endpoints)
        .filter(models.Endpoints.endpoint == endpoint_data["endpoint"])
        .first()
    )

    if not endpoint:
        instance = utils.create_endpoint(endpoint_data)
        new_endpoint = models.Endpoints(**instance.__dict__)
        db.add(new_endpoint)
        db.commit()
        db.refresh(new_endpoint)
        return {"status": "ok", "endpoint": new_endpoint}

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={"message": "Duplicated Endpoint"},
    )


@router.put("/{endpoint_id}", status_code=status.HTTP_200_OK)
def update_endpoint(endpoint_id: int, data: AddEndpoint, db: Session = Depends(get_db)):
    db_data = db.query(models.Endpoints).filter(models.Endpoints.id == endpoint_id)
    if db_data.first():
        db_datas = db_data.first()
        req_data = data.model_dump()
        if req_data["endpoint"] != db_datas.endpoint:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Endpoint URL do not match",
            )
        modified_endpoint = utils.create_endpoint(req_data)
        db_data.update(modified_endpoint.__dict__, synchronize_session=False)
        db.commit()
        return {"status": True}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Not Found"}
    )


@router.get("/{endpoint_id}", response_model=AddEndpointResponse)
async def get_endpoint(
    request: Request, endpoint_id: int, db: Session = Depends(get_db)
):
    endpoint_data = (
        db.query(models.Endpoints).filter(models.Endpoints.id == endpoint_id).first()
    )
    if endpoint_data:
        return {"status": "ok", "endpoint": endpoint_data}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Not Found"}
    )


@router.delete("/{endpoint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_endpoint(
    request: Request, endpoint_id: int, db: Session = Depends(get_db)
):
    endpoint_data = db.query(models.Endpoints).filter(
        models.Endpoints.id == endpoint_id
    )
    if endpoint_data.first():
        endpoint_data.delete(synchronize_session=False)
        db.commit()
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Not Found"}
    )
