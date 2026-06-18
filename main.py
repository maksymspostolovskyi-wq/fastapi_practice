from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from models import Base
from routers.posts import router as posts_router
from settings.db import engine, ping


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Підключаємо CRUD-модуль статей блогу
app.include_router(posts_router)


@app.get("/")
def index_root():
    return {"message": "Hello World!"}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def db_healthcheck():
    is_alive = await ping()
    if not is_alive:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        )
    return {"status": "healthy", "database": "connected"}
