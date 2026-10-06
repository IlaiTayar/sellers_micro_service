import httpx
from typing import Optional

from fastapi import HTTPException

from database import config


async def _get_from_customer_service(url: str, params: Optional[dict] = None) -> int:

    headers = {"X-Internal-Api-Key": config.INTERNAL_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, params=params, headers=headers)

    except (httpx.ConnectError, httpx.TimeoutException) as err:
        raise HTTPException(
            status_code=503,
            detail=f"Customer Service unavailable: {err}"
        )

    except httpx.HTTPError as err:
        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with Customer Service: {err}"
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail="Customer Service returned an error"
        )

    return int(response.json())


async def count_orders_referencing_item_name(item_name: str) -> int:
    url = f"{config.CUSTOMER_SERVICE_BASE_URL}/order/references"

    return await _get_from_customer_service(url, params={"item_name": item_name})


async def count_favorites_referencing_item_id(item_id: int) -> int:
    url = f"{config.CUSTOMER_SERVICE_BASE_URL}/customer-favorite-item/references"

    return await _get_from_customer_service(url, params={"item_id": item_id})
