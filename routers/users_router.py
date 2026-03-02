from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from data_sources.users_data_source import UsersDataSource
from data_sources.dependencies import get_users_datasource
from database import get_db
from models.users import UserCreate, UserResponse

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    users: Annotated[UsersDataSource, Depends(get_users_datasource)],
):
    return await users.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    users: Annotated[UsersDataSource, Depends(get_users_datasource)],
):
    return await users.get_user(user_id)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    payload: UserCreate,
    users: Annotated[UsersDataSource, Depends(get_users_datasource)],
):
    return await users.create_user(payload.username, payload.email)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    payload: UserCreate,
    users: Annotated[UsersDataSource, Depends(get_users_datasource)],
):
    updated = await users.update_user(user_id, payload.model_dump())
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    users: Annotated[UsersDataSource, Depends(get_users_datasource)],
):
    ok = await users.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
