from typing import List, Optional, Union

from api.internal_api.customer_service import customer_service_api
from model.exception_handler_model.item_exception import ItemException
from model.item import Item
from repository import item_repository, seller_repository


async def create_item(item: Item) -> int:
    return await item_repository.create_item(item)


async def update_item_by_id(item_id: int, item: Item) -> Union[Item, ItemException]:
    existing_item = await get_item_by_id(item_id)
    if isinstance(existing_item, ItemException):
        return existing_item

    item.item_id = item_id
    await item_repository.update_item_by_id(item_id, item)
    return item


async def get_item_by_id(item_id: int) -> Union[Item, ItemException]:
    item = await item_repository.get_item_by_id(item_id)
    if item is None:
        return ItemException.ITEM_NOT_FOUND

    return item


async def get_all_items() -> List[Item]:
    return await item_repository.get_all_items()


async def get_item_by_name(
    item_name: str,
    seller_name: Optional[str] = None
) -> Union[Item, ItemException]:
    seller_id: Optional[int] = None

    if seller_name is not None:
        seller = await seller_repository.get_seller_by_name(seller_name)
        if seller is None:
            return ItemException.ITEM_NOT_FOUND

        seller_id = seller.seller_id

    item = await item_repository.get_item_by_name(item_name, seller_id)
    if item is None:
        return ItemException.ITEM_NOT_FOUND

    return item


async def delete_item_by_id(item_id: int) -> Union[str, ItemException]:
    existing_item = await get_item_by_id(item_id)
    if isinstance(existing_item, ItemException):
        return existing_item

    order_references = await customer_service_api.count_orders_referencing_item_id(item_id)
    favorite_references = await customer_service_api.count_favorites_referencing_item_id(item_id)

    if order_references > 0 or favorite_references > 0:
        return ItemException.ITEM_IN_USE

    await item_repository.delete_item_by_id(item_id)
    return f"item with id: {item_id} was successfully deleted"
