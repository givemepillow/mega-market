from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.params import Path
from fastapi.responses import Response

from market.api import schemas, handlers
from market.api.handlers import tools

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
async def nodes(uuid: UUID = Path(..., alias='id')):
    return await handlers.nodes.handle(uuid)


@router.get("/sales", response_model=schemas.ShopUnitStatisticResponse)
async def sales(current_datetime: str = Query(..., alias='date')):
    return await handlers.sales.handle(tools.to_datetime(current_datetime))


@router.get("/node/{id}/statistic", response_model=schemas.ShopUnitStatisticResponse)
async def statistic(
        uuid: UUID = Path(alias='id'),
        start: str = Query(None, alias='dateStart'),
        end: str = Query(None, alias='dateEnd')
):
    return await handlers.statistic.handle(
        uuid,
        tools.to_datetime(start) if start else None,
        tools.to_datetime(end) if end else None
    )
