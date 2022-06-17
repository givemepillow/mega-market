from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from market.api.endpoints import router
from market.db.orm import Engine
from market.db.model import Base
from market.api import reponses

app = FastAPI()
app.include_router(router, tags=['MEGA MARKET API'])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(*_):
    """
    Подменяет код и тело ответа при RequestValidationError на 400 и JSON
    согласно описанию в openapi.yaml соответственно.
    :return: market.api.schemas.Error
    """
    return reponses.VALIDATION_FAILED


@app.on_event("startup")
async def startup_event():
    async with Engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_event():
    await Engine.dispose()
