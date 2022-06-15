from __future__ import annotations

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


class AbstractShopUnit(BaseModel):
    pass


class ShopUnit(BaseModel):
    id: UUID
    name: str
    date: datetime
    parentId: Optional[UUID]
    type: ShopUnitType
    price: Optional[int]
    children: Optional[list[ShopUnit]]


class Error(BaseModel):
    code: int
    message: str
