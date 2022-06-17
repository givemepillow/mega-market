from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

VALIDATION_FAILED = JSONResponse(
    status_code=status.HTTP_400_BAD_REQUEST,
    content=jsonable_encoder(
        {"code": status.HTTP_400_BAD_REQUEST, "message": "Validation Failed"}
    )
)
