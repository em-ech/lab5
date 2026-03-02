from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from data_sources.bikes_data_source import BikesDataSource
from data_sources.users_data_source import UsersDataSource


def get_bikes_datasource(db: AsyncSession = Depends(get_db)) -> BikesDataSource:
    return BikesDataSource(db)


def get_users_datasource(db: AsyncSession = Depends(get_db)) -> UsersDataSource:
    return UsersDataSource(db)
