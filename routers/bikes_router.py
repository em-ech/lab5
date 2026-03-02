from __future__ import annotations

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List, Optional

from data_sources.bikes_data_source import BikesDataSource
from data_sources.dependencies import get_bikes_datasource
from database import get_db
from db_models import Bike
from models.bikes import BikeCreate, BikeResponse

router = APIRouter()


@router.get("/", response_model=List[BikeResponse])
async def get_bikes(
    bikes: Annotated[BikesDataSource, Depends(get_bikes_datasource)],
    status: Optional[str] = Query(None, description="Filter bikes by status"),
):
    all_bikes = await bikes.get_all_bikes()
    if status:
        all_bikes = [b for b in all_bikes if b.status == status]
    return all_bikes


@router.get("/{bike_id}", response_model=BikeResponse)
async def get_bike_detail(
    bike_id: int,
    bikes: Annotated[BikesDataSource, Depends(get_bikes_datasource)],
):
    return await bikes.get_bike(bike_id)


@router.post("/", response_model=BikeResponse, status_code=201)
async def create_bike(
    payload: BikeCreate,
    db: AsyncSession = Depends(get_db),
):
    bike = Bike(
        model=payload.model,
        battery_level=payload.battery_level,
        status=payload.status,
    )
    db.add(bike)
    await db.commit()
    await db.refresh(bike)
    return bike


@router.put("/{bike_id}", response_model=BikeResponse)
async def update_bike(
    bike_id: int,
    payload: BikeCreate,
    bikes: Annotated[BikesDataSource, Depends(get_bikes_datasource)],
):
    updated = await bikes.update_bike(
        bike_id,
        {
            "model": payload.model,
            "battery_level": payload.battery_level,
            "status": payload.status,
        },
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Bike not found")
    return updated


@router.delete("/{bike_id}")
async def delete_bike(
    bike_id: int,
    bikes: Annotated[BikesDataSource, Depends(get_bikes_datasource)],
):
    ok = await bikes.delete_bike(bike_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Bike not found")
    return {"message": "Bike deleted"}
