from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from loguru import logger

from market.api.endpoints import router
from market.db.orm import Engine
from market.db.model import Base
import os

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import command, config

from market.api import reponses
from market.api.handlers.exceptions import ValidationFailed400, ItemNotFound404

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Подменяет код и тело ответа при RequestValidationError на 400 и JSON
    согласно описанию в openapi.yaml соответственно.
    :return: HTTP 400 BAD REQUEST: {"code": 400, "message": "Validation Failed"}
    """
    logger.info(f"{request.method} {request.url.path}: {exc}", )
    return reponses.VALIDATION_FAILED


@app.exception_handler(ValidationFailed400)
async def validation_exception_handler(request: Request, exc: ValidationFailed400):
    """
    Отлавливает ValidationFailed400 исключения и возвращает код и JSON
    согласно описанию в openapi.yaml.
    :return: HTTP 400 BAD REQUEST: {"code": 400, "message": "Validation Failed"}
    """
    logger.info(f"{request.method} {request.url.path}: {exc}", )
    return reponses.VALIDATION_FAILED


@app.exception_handler(ItemNotFound404)
async def not_found_exception_handler(request: Request, exc: ItemNotFound404):
    """
    Отлавливает ItemNotFound404 исключения и возвращает код и JSON
    согласно описанию в openapi.yaml.
    :return: HTTP 404 NOT FOUND: {"code": 404, "message": "Item not found"}
    """
    logger.info(f"{request.method} {request.url.path}: {exc}", )
    return reponses.ITEM_NOT_FOUND


app.include_router(router, tags=['MEGA MARKET API'])

logger.remove()
logger.add(
    'logfile.log',
    rotation='1MB',
    compression='zip',
    format="{time:MMM DD HH:mm:ss}: {message}"
)
