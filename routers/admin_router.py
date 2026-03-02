from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Annotated

from data_sources.bikes_data_source import BikesDataSource
from data_sources.users_data_source import UsersDataSource
from data_sources.dependencies import get_bikes_datasource, get_users_datasource


def verify_admin_key(api_key: str = Header()):
    if api_key != "eco_admin_secret":
        raise HTTPException(status_code=403, detail="Invalid or missing admin API key")


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_admin_key)],
)


@router.get("/stats")
async def get_admin_stats(
    bikes: Annotated[BikesDataSource, Depends(get_bikes_datasource)],
    users: Annotated[UsersDataSource, Depends(get_users_datasource)],
):
    all_bikes = await bikes.get_all_bikes()
    all_users = await users.get_all_users()

    return {
        "total_bikes": len(all_bikes),
        "active_rentals": len([b for b in all_bikes if b.status == "rented"]),
        "registered_users": len(all_users),
    }
