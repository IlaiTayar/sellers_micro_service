import json
from typing import Optional, List

from database import database
from databases.interfaces import Record
from model.item import Item
from repository import cache_repository

TABLE_NAME = "item"


def _to_item(record: Record) -> Item:
    return Item(
        item_id=record["item_id"],
        seller_id=record["seller_id"],
        item_name=record["item_name"],
        price=record["price"]
    )

async def create_item(item: Item) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} (seller_id, item_name, price)
        VALUES (:seller_id, :item_name, :price)
    """

    values = {"seller_id": item.seller_id,
              "item_name": item.item_name,
              "price": item.price
              }

    return await database.execute(query, values)


async def update_item_by_id(item_id: int, item: Item) -> None:
    if cache_repository.is_key_exists(str(item_id)):
        cache_repository.remove_cache_entity(str(item_id))

    query = f"""
        UPDATE {TABLE_NAME}
        SET seller_id = :seller_id,
            item_name = :item_name,
            price = :price
        WHERE item_id = :item_id
    """

    values = {
        "item_id": item_id,
        "seller_id": item.seller_id,
        "item_name": item.item_name,
        "price": item.price,
    }

    await database.execute(query, values)


async def get_item_by_id(item_id: int) -> Optional[Item]:
    if cache_repository.is_key_exists(str(item_id)):
        str_item = cache_repository.get_cache_entity(str(item_id))

        if str_item:
            item = _to_item(json.loads(str_item))
            cache_repository.remove_cache_entity(str(item_id))
            cache_repository.create_cache_entity(str(item_id), item.model_dump_json())
            return item

        return None

    query = f"SELECT * FROM {TABLE_NAME} WHERE item_id=:item_id"

    record: Optional[Record] = await database.fetch_one(query, values={"item_id": item_id})
    if record:
        item = _to_item(record)
        cache_repository.create_cache_entity(str(item_id), item.model_dump_json())
        return item

    return None


async def get_item_by_name(item_name: str) -> Optional[Item]:
    query = f"""
        SELECT * FROM {TABLE_NAME}
        WHERE item_name = :item_name
        ORDER BY price ASC
        LIMIT 1
    """

    record: Optional[Record] = await database.fetch_one(query, values={"item_name": item_name})
    return _to_item(record) if record else None


async def get_all_items() -> List[Item]:
    query = f"SELECT * FROM {TABLE_NAME}"

    records: List[Record] = await database.fetch_all(query)

    return [_to_item(record) for record in records]


async def delete_item_by_id(item_id: int) -> None:
    if cache_repository.is_key_exists(str(item_id)):
        cache_repository.remove_cache_entity(str(item_id))

    query = f"DELETE FROM {TABLE_NAME} WHERE item_id=:item_id"

    await database.execute(query, values={"item_id": item_id})