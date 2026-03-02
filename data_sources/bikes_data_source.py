from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db_models import Bike  # if your class is named BikeDB, change this import


class BikesDataSource:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_bikes(self) -> List[Bike]:
        """Retrieve all bikes."""
        result = await self.db.execute(select(Bike))
        return result.scalars().all()

    async def get_bike(self, bike_id: int) -> Bike:
        """Retrieve a single bike by ID."""
        # 1. Async Query: Find the bike
        # Equivalent to: SELECT * FROM bikes WHERE id = X
        result = await self.db.execute(
            select(Bike).where(Bike.id == bike_id)
        )
        bike = result.scalar_one_or_none()

        if not bike:
            raise HTTPException(status_code=404, detail="Bike not found")

        # 2. Check Status
        if bike.status != "available":
            raise HTTPException(status_code=400, detail="Bike not available")

        return bike

    async def update_bike(
        self,
        bike_id: int,
        update_data: dict
    ) -> Optional[Bike]:
        """Update a bike. Returns the updated bike or None if not found."""
        result = await self.db.execute(
            select(Bike).where(Bike.id == bike_id)
        )
        bike = result.scalar_one_or_none()

        if not bike:
            return None

        # 2. Update fields
        for key, value in update_data.items():
            setattr(bike, key, value)

        # 3. Save to DB
        await self.db.commit()
        await self.db.refresh(bike)

        return bike

    async def delete_bike(self, bike_id: int) -> bool:
        """Delete a bike. Returns True if deleted, False if not found."""
        result = await self.db.execute(
            select(Bike).where(Bike.id == bike_id)
        )
        bike = result.scalar_one_or_none()

        if not bike:
            return False

        await self.db.delete(bike)
        await self.db.commit()
        return True