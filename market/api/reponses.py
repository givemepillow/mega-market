from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

VALIDATION_FAILED = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content=jsonable_encoder(
        {"code": status.HTTP_400_BAD_REQUEST, "message": "Validation Failed"}
    )
)

ITEM_NOT_FOUND = JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content=jsonable_encoder(
        {"code": status.HTTP_404_NOT_FOUND, "message": "Item not found"}
    )
)
