from contextlib import asynccontextmanager

from fastapi import FastAPI

from api_v1.api_router import router
from database.db import engine
from database.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan, title='Kitten Show')

app.include_router(router)
