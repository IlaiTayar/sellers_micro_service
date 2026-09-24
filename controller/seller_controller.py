from typing import List, Optional

from fastapi import APIRouter, HTTPException
from model.seller import Seller
from service import seller_service

router = APIRouter(
    prefix="/seller",
    tags=["seller"]
)


@router.post("/create", status_code=201)
async def create_seller(seller: Seller) -> int:
    return await seller_service.create_seller(seller)


@router.put("/update-{seller_id}", status_code=200)
async def update_seller_by_id(seller_id: int, seller: Seller) -> Seller:
    result = await seller_service.update_seller_by_id(seller_id, seller)
    if not result:
        raise HTTPException(status_code=404, detail=f"Seller with id: {seller_id} Not Found")

    return result


@router.get("/get-{seller_id}", response_model=Seller, status_code=200)
async def get_seller_by_id(seller_id: int) -> Seller:
    result = await seller_service.get_seller_by_id(seller_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Seller with id: {seller_id} Not Found")

    return result


@router.get("/get/all", response_model=List[Seller], status_code=200)
async def get_all_sellers() -> List[Seller]:
    return await seller_service.get_all_sellers()


@router.delete("/{seller_id}", status_code=200)
async def delete_seller_by_id(seller_id: int) -> str:
    result = await seller_service.delete_seller_by_id(seller_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Seller with id: {seller_id} Not Found")

    return result