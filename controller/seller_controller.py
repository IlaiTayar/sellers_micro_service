from typing import Any, List, Union

from fastapi import APIRouter, HTTPException

from model.exception_handler_model.seller_exception import SellerException
from model.seller import Seller
from service import seller_service

router = APIRouter(
    prefix="/seller",
    tags=["seller"]
)


def _exception_handler(result: Any) -> Any:
    if isinstance(result, SellerException):

        if result == SellerException.SELLER_NOT_FOUND:
            raise HTTPException(status_code=404, detail=f"{SellerException.SELLER_NOT_FOUND}")

        if result == SellerException.SELLER_HAS_REFERENCED_ITEMS:
            raise HTTPException(status_code=409, detail=f"{SellerException.SELLER_HAS_REFERENCED_ITEMS} - one or more items are still referenced by customer orders or favorites")

    return result


@router.post("/create", status_code=201)
async def create_seller(seller: Seller) -> int:
    return await seller_service.create_seller(seller)


@router.put("/update-{seller_id}", status_code=200)
async def update_seller_by_id(seller_id: int, seller: Seller) -> Seller:
    result: Union[Seller, SellerException] = await seller_service.update_seller_by_id(seller_id, seller)

    return _exception_handler(result)


@router.get("/get-{seller_id}", response_model=Seller, status_code=200)
async def get_seller_by_id(seller_id: int) -> Seller:
    result: Union[Seller, SellerException] = await seller_service.get_seller_by_id(seller_id)

    return _exception_handler(result)


@router.get("/get/all", response_model=List[Seller], status_code=200)
async def get_all_sellers() -> List[Seller]:
    return await seller_service.get_all_sellers()


@router.delete("/{seller_id}", status_code=200)
async def delete_seller_by_id(seller_id: int) -> str:
    result: Union[str, SellerException] = await seller_service.delete_seller_by_id(seller_id)

    return _exception_handler(result)
