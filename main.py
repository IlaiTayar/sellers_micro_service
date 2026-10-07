from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from controller.seller_controller import router as seller_router
from controller.item_cotroller import router as item_router
from database import database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await database.connect()
    print("Database connected")
    yield
    await database.disconnect()
    print("Database disconnected")


app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(seller_router)
app.include_router(item_router)
