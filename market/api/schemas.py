from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class BaseModelConfig(BaseModel):
    class Config:
        allow_population_by_field_name = True

        json_encoders = {
            datetime: lambda dt: dt.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        }


class ShopUnitType(str, Enum):
    OFFER: str = 'OFFER'
    CATEGORY: str = 'CATEGORY'


class ShopUnitImport(BaseModelConfig):
    id: UUID
    parent_id: Optional[UUID] = Field(alias='parentId')
    name: str = Field(min_length=1)
    type: ShopUnitType
    price: Optional[int] = Field(gt=-1)

    class Config:
        use_enum_values = True


class ShopUnitImportRequest(BaseModelConfig):
    items: list[ShopUnitImport]
    update_date: datetime = Field(alias='updateDate')


class ShopUnit(BaseModelConfig):
    id: UUID
    name: str = Field(min_length=1)
    date: datetime
    parent_id: Optional[UUID] = Field(alias='parentId')
    type: ShopUnitType
    price: Optional[int] = Field(gt=-1)
    children: Optional[list['ShopUnit']]


class ShopUnitStatisticUnit(BaseModelConfig):
    id: UUID
    name: str = Field(min_length=1)
    parent_id: Optional[UUID] = Field(alias='parentId')
    type: ShopUnitType
    price: Optional[int] = Field(gt=-1)
    date: datetime


class ShopUnitStatisticResponse(BaseModelConfig):
    items: list[ShopUnitStatisticUnit]
