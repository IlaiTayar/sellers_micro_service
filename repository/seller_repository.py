from typing import Optional, List

from database import database
from databases.interfaces import Record
from model.seller import Seller


TABLE_NAME = "seller"


def _to_seller(record: Record) -> Seller:
    return Seller(
        seller_id=record["seller_id"],
        seller_name=record["seller_name"],
        email=record["email"],
        status=record["status"]
    )


async def create_seller(seller: Seller) -> int:
    query = f"""
        INSERT INTO {TABLE_NAME} (seller_name, email, status)
        VALUES (:seller_name, :email, :status)
    """

    values = {"seller_name": seller.seller_name,
              "email": seller.email,
              "status": seller.status.value}

    return await database.execute(query, values)


async def update_seller_by_id(seller_id: int, seller: Seller) -> None:
    query = f"""
        UPDATE {TABLE_NAME}
        SET seller_name = :seller_name,
            email = :email,
            status = :status
        WHERE seller_id = :seller_id
    """
    values = {
        "seller_id": seller_id,
        "seller_name": seller.seller_name,
        "email": seller.email,
        "status": seller.status.value
    }

    await database.execute(query, values)


async def get_seller_by_id(seller_id: int) -> Optional[Seller]:
    query = f"""
    SELECT * FROM {TABLE_NAME} WHERE seller_id=:seller_id
    """

    record: Optional[Record] = await database.fetch_one(query, values={"seller_id": seller_id})

    return _to_seller(record) if record else None


async def get_seller_by_email(email: str) -> Optional[Seller]:
    query = f"""
    SELECT * FROM {TABLE_NAME} WHERE email=:email
    """

    record: Optional[Record] = await database.fetch_one(query, values={"email": email})

    return _to_seller(record) if record else None


async def get_all_sellers() -> List[Seller]:
    query = f"SELECT * FROM {TABLE_NAME}"

    records: List[Record] = await database.fetch_all(query)

    return [_to_seller(record) for record in records]


async def delete_seller_by_id(seller_id: int) -> None:
    query = f"DELETE FROM {TABLE_NAME} WHERE seller_id=:seller_id"

    await database.execute(query, values={"seller_id": seller_id})