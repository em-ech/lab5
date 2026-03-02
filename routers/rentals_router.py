from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from db_models import Bike, Rental, User
from models.rentals import RentalProcessing

router = APIRouter()


@router.post("/", status_code=201)
async def create_rental(
    payload: RentalProcessing,
    db: AsyncSession = Depends(get_db),
):
    # 1. Verify user exists
    user = (await db.execute(select(User).where(User.id == payload.user_id))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Verify bike exists
    bike = (await db.execute(select(Bike).where(Bike.id == payload.bike_id))).scalar_one_or_none()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")

    # 3. Business rules: available + battery
    if bike.status != "available":
        raise HTTPException(status_code=400, detail="Bike not available")

    if bike.battery_level < 20:
        raise HTTPException(status_code=400, detail="Bike battery too low for rental")

    # 4. Create rental and update bike status in a single transaction
    rental = Rental(bike_id=bike.id, user_id=user.id)
    bike.status = "rented"

    db.add(rental)
    await db.commit()
    await db.refresh(rental)

    return {
        "message": "Rental created successfully",
        "rental_id": rental.id,
        "bike_id": payload.bike_id,
        "user_id": payload.user_id,
    }
