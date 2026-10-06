from typing import List, Optional, Union

from api.internal_api.customer_service import customer_service_api
from model.exception_handler_model.seller_exception import SellerException
from model.seller import Seller
from notification import notification_service
from repository import item_repository, seller_repository


async def create_seller(seller: Seller) -> int:
    return await seller_repository.create_seller(seller)


async def update_seller_by_id(seller_id: int, seller: Seller) -> Union[Seller, SellerException]:
    existing_seller: Union[Seller, SellerException] = await get_seller_by_id(seller_id)
    if isinstance(existing_seller, SellerException):
        return existing_seller

    await seller_repository.update_seller_by_id(seller_id, seller)
    return seller


async def get_seller_by_id(seller_id: int) -> Union[Seller, SellerException]:
    seller: Optional[Seller] = await seller_repository.get_seller_by_id(seller_id)
    if seller is None:
        return SellerException.SELLER_NOT_FOUND

    return seller


async def get_seller_by_name(seller_name: str) -> Union[Seller, SellerException]:
    seller: Optional[Seller] = await seller_repository.get_seller_by_name(seller_name)
    if seller is None:
        return SellerException.SELLER_NOT_FOUND

    return seller


async def get_seller_by_email(email: str) -> Union[Seller, SellerException]:
    seller: Optional[Seller] = await seller_repository.get_seller_by_email(email)
    if seller is None:
        return SellerException.SELLER_NOT_FOUND

    return seller


async def get_all_sellers() -> List[Seller]:
    return await seller_repository.get_all_sellers()


async def delete_seller_by_id(seller_id: int) -> Union[str, SellerException]:
    existing_seller: Union[Seller, SellerException] = await get_seller_by_id(seller_id)
    if isinstance(existing_seller, SellerException):
        return existing_seller

    seller_items = await item_repository.get_items_by_seller_id(seller_id)

    for item in seller_items:
        order_references = await customer_service_api.count_orders_referencing_item_id(item.item_id)
        favorite_references = await customer_service_api.count_favorites_referencing_item_id(item.item_id)

        if order_references > 0 or favorite_references > 0:
            notification_service.notify_seller(
                seller_id,
                f"your account was not deleted because item '{item.item_name}' (id: {item.item_id}) is still referenced by customer orders or favorites"
            )
            return SellerException.SELLER_HAS_REFERENCED_ITEMS

    for item in seller_items:
        await item_repository.delete_item_by_id(item.item_id)

    if seller_items:
        notification_service.notify_seller(
            seller_id,
            f"your account was deleted along with {len(seller_items)} item(s)"
        )

    await seller_repository.delete_seller_by_id(seller_id)
    return f"seller with id: {seller_id} deleted successfully"
