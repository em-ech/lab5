from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Bike, User


async def seed_if_empty(db: AsyncSession) -> None:
    bikes_exist = (await db.execute(select(Bike).limit(1))).scalar_one_or_none()
    users_exist = (await db.execute(select(User).limit(1))).scalar_one_or_none()

    if not bikes_exist:
        db.add_all(
            [
                Bike(model="EcoCruiser", status="available", battery_level=95, ),
                Bike(model="MountainE", status="maintenance", battery_level=15, ),
                Bike(model="CitySprint", status="rented", battery_level=60, ),
            ]
        )

    if not users_exist:
        db.add_all(
            [
                User(username="alice", email="alice@example.com", is_active=True),
                User(username="bob", email="bob@example.com", is_active=True),
            ]
        )

    if not bikes_exist or not users_exist:
        await db.commit()
