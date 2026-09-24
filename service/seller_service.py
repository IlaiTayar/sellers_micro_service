from typing import List, Optional

from model.seller import Seller
from repository import seller_repository


async def create_seller(seller: Seller) -> int:
    return await seller_repository.create_seller(seller)


async def update_seller_by_id(seller_id: int, seller: Seller) -> Optional[Seller]:
    existing_seller: Optional[Seller] = await get_seller_by_id(seller_id)
    if existing_seller is None:
        return None

    await seller_repository.update_seller_by_id(seller_id, seller)
    return seller


async def get_seller_by_id(seller_id: int) -> Optional[Seller]:
    seller: Optional[Seller] = await seller_repository.get_seller_by_id(seller_id)

    if seller is None:
        return None

    return seller


async def get_all_sellers() -> List[Seller]:
    return await seller_repository.get_all_sellers()


async def delete_seller_by_id(seller_id: int) -> Optional[str]:
    existing_seller: Optional[Seller] = await get_seller_by_id(seller_id)
    if not existing_seller:
        return None

    await seller_repository.delete_seller_by_id(seller_id)
    return f"seller with id: {seller_id} deleted successfully"