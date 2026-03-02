from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import engine
from db_models import Base
from seed import seed_if_empty
from routers import bikes_router, users_router, rentals_router, admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Optional seed for local testing
    from database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        await seed_if_empty(db)

    yield

    # Close connections on shutdown
    await engine.dispose()


app = FastAPI(
    title="EcoMute Core",
    description="Backend API for the EcoMute Bike Sharing Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(
    bikes_router.router,
    prefix="/bikes",
    tags=["Bikes"],
    responses={404: {"description": "Bike Not Found"}},
)

app.include_router(
    users_router.router,
    prefix="/users",
    tags=["Users"],
)

app.include_router(
    rentals_router.router,
    prefix="/rentals",
    tags=["Rentals"],
)

app.include_router(
    admin_router.router,
)


@app.get("/")
async def root():
    return {"message": "Welcome to EcoMute. Go to /docs for Swagger UI"}
