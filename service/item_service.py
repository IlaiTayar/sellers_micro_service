from typing import List, Optional

from model.item import Item
from repository import item_repository


async def create_item(item: Item) -> int:
    return await item_repository.create_item(item)


async def update_item_by_id(item_id: int, item: Item) -> Optional[Item]:
    existing_item: Optional[Item] = await get_item_by_id(item_id)
    if not existing_item:
        return None

    await item_repository.update_item_by_id(item_id, item)
    return item


async def get_item_by_id(item_id: int) -> Optional[Item]:
    item: Optional[Item] = await item_repository.get_item_by_id(item_id)
    if item is None:
        return None

    return item


async def get_all_items() -> List[Item]:
    return await item_repository.get_all_items()


async def get_item_by_name(item_name: str) -> Optional[Item]:
    item: Optional[Item] = await item_repository.get_item_by_name(item_name)
    if item is None:
        return None

    return item


async def delete_item_by_id(item_id: int) -> Optional[str]:
    existing_item: Optional[Item] = await get_item_by_id(item_id)
    if not existing_item:
        return None

    await item_repository.delete_item_by_id(item_id)
    return f"item with id: {item_id} was successfully deleted"