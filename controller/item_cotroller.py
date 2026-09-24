from typing import List

from fastapi import APIRouter, HTTPException
from model.item import Item
from service import item_service

router = APIRouter(
    prefix="/item",
    tags=["item"]
)


@router.post("/create", status_code=201)
async def create_item(item: Item) -> int:
    return await item_service.create_item(item)


@router.put("/update-{item_id}", response_model=Item ,status_code=200)
async def update_item_by_id(item_id: int, item: Item) -> Item:
    result = await item_service.update_item_by_id(item_id, item)
    if not result:
        raise HTTPException(status_code=404, detail=f"Item with id: {item_id} not found.")

    return result


@router.get("/get-id-{item_id}", response_model=Item, status_code=200)
async def get_item_by_id(item_id: int) -> Item:
    result = await item_service.get_item_by_id(item_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Item with id: {item_id} not found.")

    return result


@router.get("/get-name-{item_name}", response_model=Item, status_code=200)
async def get_item_by_name(item_name: str) -> Item:
    result = await item_service.get_item_by_name(item_name)
    if not result:
        raise HTTPException(status_code=404, detail=f"Item with name: {item_name} not found.")

    return result


@router.get("/get-all", response_model=List[Item])
async def get_all_items() -> List[Item]:
    return await item_service.get_all_items()


@router.delete("/delete-{item_id}")
async def delete_item_by_id(item_id: int) -> str:
    result = await item_service.delete_item_by_id(item_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Item with id: {item_id} not found.")

    return result