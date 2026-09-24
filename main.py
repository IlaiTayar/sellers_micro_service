from fastapi import FastAPI
from controller.seller_controller import router as seller_router
from controller.item_cotroller import router as item_router
from database import database


app: FastAPI = FastAPI()

app.include_router(seller_router)
app.include_router(item_router)


@app.on_event("startup")
async def startup():
    await database.connect()
    print("Database connected")


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print("Database disconnected")