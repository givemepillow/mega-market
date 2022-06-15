from datetime import datetime
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Path
from fastapi.responses import Response

import schemas

router = APIRouter()


@router.post("/imports")
async def imports(shop_unit: schemas.ShopUnitImportRequest):
    ...
    return Response(status_code=200)


@router.delete("/delete/{id}")
async def delete(unit_id: UUID = Path(..., alias='id')):
    ...
    return Response(status_code=200)


@router.get("/nodes/{id}", response_model=schemas.ShopUnit)
async def nodes(unit_id: UUID = Path(..., alias='id')):
    ...


@router.get("/sales", response_model=schemas.ShopUnitStatisticResponse)
async def sales(date: datetime):
    ...
