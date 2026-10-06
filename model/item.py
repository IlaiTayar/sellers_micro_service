from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    item_id: Optional[int] = None
    seller_id: int
    item_name: str
    price: float
    image_url: Optional[str] = None