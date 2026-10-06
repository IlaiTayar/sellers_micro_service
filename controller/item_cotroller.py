from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException, Query

from model.exception_handler_model.item_exception import ItemException
from model.item import Item
from security.auth import Principal, get_current_principal, require_ownership
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


@router.post("", status_code=201)
async def create_item(item: Item, principal: Principal = Depends(get_current_principal)) -> int:
    item.seller_id = principal.principal_id
    return await item_service.create_item(item)


@router.get("", response_model=List[Item], status_code=200)
async def get_all_items() -> List[Item]:
    return await item_service.get_all_items()


@router.get("/by-name", response_model=Item, status_code=200)
async def get_item_by_name(item_name: str = Query(...)) -> Item:
    result: Union[Item, ItemException] = await item_service.get_item_by_name(item_name)

    return _exception_handler(result)


@router.get("/{item_id}", response_model=Item, status_code=200)
async def get_item_by_id(item_id: int) -> Item:
    result: Union[Item, ItemException] = await item_service.get_item_by_id(item_id)

    return _exception_handler(result)


@router.put("/{item_id}", response_model=Item, status_code=200)
async def update_item_by_id(item_id: int, item: Item, principal: Principal = Depends(get_current_principal)) -> Item:
    existing_item: Union[Item, ItemException] = await item_service.get_item_by_id(item_id)
    existing_item = _exception_handler(existing_item)
    require_ownership(principal, existing_item.seller_id)

    item.seller_id = principal.principal_id

    result: Union[Item, ItemException] = await item_service.update_item_by_id(item_id, item)

    return _exception_handler(result)


@router.delete("/{item_id}", status_code=200)
async def delete_item_by_id(item_id: int, principal: Principal = Depends(get_current_principal)) -> str:
    existing_item: Union[Item, ItemException] = await item_service.get_item_by_id(item_id)
    existing_item = _exception_handler(existing_item)
    require_ownership(principal, existing_item.seller_id)

    result: Union[str, ItemException] = await item_service.delete_item_by_id(item_id)

    return _exception_handler(result)
