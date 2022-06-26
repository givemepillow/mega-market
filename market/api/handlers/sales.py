from datetime import datetime
from typing import Dict

from market.api.handlers import tools
from market.db.orm import Session
from market.db import crud


async def handle(current_datetime: datetime) -> Dict:
    """
    Возвращает товары, цена которых была обновлена за 24 часа до переданной даты.
    """
    async with Session() as s:
        offers = await crud.Offer.get_for_24_hours(current_datetime, s)
        return dict(items=[tools.stat_to_response_dict(o, 'OFFER') for o in offers])
