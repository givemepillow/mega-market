from fastapi import APIRouter
from fastapi.responses import Response

import schemas

router = APIRouter()


@router.post("/imports")
async def imports(shop_unit: schemas.ShopUnitImportRequest):
    ...
    return Response(status_code=200)
