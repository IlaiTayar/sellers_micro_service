from enum import Enum
from typing import Optional

from pydantic import BaseModel

class SellerStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Seller(BaseModel):
    seller_id: Optional[int] = None
    seller_name: str
    email:str
    status: SellerStatus = SellerStatus.ACTIVE