from datetime import datetime
from uuid import UUID

from market.api.handlers import tools
from market.api.handlers.exceptions import ItemNotFound404
from market.db.orm import Session
from market.db import crud
from market.api.schemas import ShopUnitType


async def handle(uuid: UUID, start: datetime, end: datetime):
    """
    Возвращает статистику изменений юнита за указанный период от - до.
    :raises ItemNotFound404 в случае если в БД не юнита с переданными uuid.
    """
    async with Session() as s:
        unit = await crud.ShopUnit.get(uuid, s)
        if not unit:
            raise ItemNotFound404(f'unit with uuid "{uuid}" does not exist')
        if unit.type == ShopUnitType.CATEGORY:
            history = await crud.History.of_category_between_datetime(uuid, start, end, s)
        else:
            history = await crud.History.of_offers_between_datetime(uuid, start, end, s)
        return dict(items=[tools.stat_to_response_dict(u, unit.type) for u in history])
