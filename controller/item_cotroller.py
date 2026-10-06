from typing import Any, List, Union

from fastapi import APIRouter, HTTPException

from model.exception_handler_model.item_exception import ItemException
from model.item import Item
from service import item_service

router = APIRouter(
    prefix="/item",
    tags=["item"]
)


def _exception_handler(result: Any) -> Any:
    if isinstance(result, ItemException):

        if result == ItemException.ITEM_NOT_FOUND:
            raise HTTPException(status_code=404, detail=f"{ItemException.ITEM_NOT_FOUND}")

        if result == ItemException.ITEM_IN_USE:
            raise HTTPException(status_code=409, detail=f"{ItemException.ITEM_IN_USE} - referenced by customer orders or favorites")

    return result


@router.post("/create", status_code=201)
async def create_item(item: Item) -> int:
    return await item_service.create_item(item)


@router.put("/update-{item_id}", response_model=Item, status_code=200)
async def update_item_by_id(item_id: int, item: Item) -> Item:
    result: Union[Item, ItemException] = await item_service.update_item_by_id(item_id, item)

    return _exception_handler(result)


@router.get("/get-id-{item_id}", response_model=Item, status_code=200)
async def get_item_by_id(item_id: int) -> Item:
    result: Union[Item, ItemException] = await item_service.get_item_by_id(item_id)

    return _exception_handler(result)


@router.get("/get-name-{item_name}", response_model=Item, status_code=200)
async def get_item_by_name(item_name: str) -> Item:
    result: Union[Item, ItemException] = await item_service.get_item_by_name(item_name)

    return _exception_handler(result)


@router.get("/get-all", response_model=List[Item])
async def get_all_items() -> List[Item]:
    return await item_service.get_all_items()


@router.delete("/delete-{item_id}")
async def delete_item_by_id(item_id: int) -> str:
    result: Union[str, ItemException] = await item_service.delete_item_by_id(item_id)

    return _exception_handler(result)
