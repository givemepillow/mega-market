from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class ShopUnitType(str, Enum):
    OFFER: str = 'OFFER'
    CATEGORY: str = 'CATEGORY'


class ShopUnitImport(BaseModel):
    id: UUID
    parent_id: Optional[UUID] = Field(alias='parentId')
    name: str = Field(min_length=1)
    type: ShopUnitType
    price: Optional[int] = Field(gt=-1)

    class Config:
        use_enum_values = True


class ShopUnitImportRequest(BaseModel):
    items: list[ShopUnitImport]
    update_date: datetime = Field(alias='updateDate')


class ShopUnit(BaseModel):
    id: UUID
    name: str = Field(min_length=1)
    date: datetime
    parent_id: Optional[UUID] = Field(alias='parentId')
    type: ShopUnitType
    price: Optional[int] = Field(gt=-1)
    children: Optional[list['ShopUnit']]


class Error(BaseModel):
    code: int
    message: str


class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str = Field(min_length=1)
    parent_id: Optional[UUID] = Field(alias='parentId')
    type: ShopUnitType
    price: Optional[int] = Field(gt=-1)
    date: datetime


class ShopUnitStatisticResponse(BaseModel):
    items: list[ShopUnitStatisticUnit]
