from pydantic import BaseModel

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class ShopUnitType(str, Enum):
    OFFER: str = 'OFFER'
    CATEGORY: str = 'CATEGORY'


class ShopUnitImport(BaseModel):
    id: UUID
    parentId: Optional[UUID]
    name: str
    type: ShopUnitType
    price: Optional[int]

    class Config:
        use_enum_values = True


class ShopUnitImportRequest(BaseModel):
    items: list[ShopUnitImport]
    updateDate: datetime
