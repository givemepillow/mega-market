from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.params import Path
from fastapi.responses import Response

from market.api import schemas, handlers

router = APIRouter()


@router.post("/imports")
async def imports(shop_unit_import: schemas.ShopUnitImportRequest):
    await handlers.imports.handle(shop_unit_import)
    return Response(status_code=200)


@router.delete("/delete/{id}")
async def delete(uuid: UUID = Path(..., alias='id')):
    await handlers.delete.handle(uuid)
    return Response(status_code=200)


@router.get("/nodes/{id}", response_model=schemas.ShopUnit)
async def nodes(unit_id: UUID = Path(..., alias='id')):
    ...


@router.get("/sales", response_model=schemas.ShopUnitStatisticResponse)
async def sales(date: datetime):
    ...


@router.get("/node/{id}/statistic", response_model=schemas.ShopUnitStatisticResponse)
async def statistic(
        unit_id: UUID = Path(alias='id'),
        date_start: datetime = Query(None, alias='dateStart'),
        date_end: datetime = Query(None, alias='dateEnd')
):
    ...
