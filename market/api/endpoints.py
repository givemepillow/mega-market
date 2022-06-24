from uuid import UUID

from fastapi import APIRouter, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.params import Path
from fastapi.responses import Response, JSONResponse

from market.api import schemas, handlers
from market.api.handlers import tools

router = APIRouter()


@router.post("/imports", status_code=status.HTTP_200_OK)
async def imports(shop_unit_import: schemas.ShopUnitImportRequest):
    await handlers.imports.handle(shop_unit_import)
    return Response(status_code=status.HTTP_200_OK)


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(uuid: UUID = Path(..., alias='id')):
    await handlers.delete.handle(uuid)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/nodes/{id}", response_model=schemas.ShopUnit, status_code=status.HTTP_200_OK)
async def nodes(uuid: UUID = Path(..., alias='id')):
    return JSONResponse(jsonable_encoder(await handlers.nodes.handle(uuid)))


@router.get("/sales", response_model=schemas.ShopUnitStatisticResponse, status_code=status.HTTP_200_OK)
async def sales(current_datetime: str = Query(..., alias='date')):
    return JSONResponse(jsonable_encoder(await handlers.sales.handle(tools.to_datetime(current_datetime))))


@router.get("/node/{id}/statistic", response_model=schemas.ShopUnitStatisticResponse, status_code=status.HTTP_200_OK)
async def statistic(
        uuid: UUID = Path(alias='id'),
        start: str = Query(None, alias='dateStart'),
        end: str = Query(None, alias='dateEnd')
):
    return JSONResponse(jsonable_encoder(await handlers.statistic.handle(
        uuid,
        tools.to_datetime(start) if start else None,
        tools.to_datetime(end) if end else None
    )))
