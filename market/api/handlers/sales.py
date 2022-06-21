from datetime import datetime, timedelta
from typing import Dict

from sqlalchemy import select

from market.api.handlers import tools
from market.db.orm import Session
from market.db import model


async def handle(current_datetime: datetime) -> Dict:
    """
    Возвращает товары, цена которых была обновлена за 24 часа до переданной даты.
    """
    async with Session() as s:
        offers = (await s.execute(
            select(model.Offer).
            where(model.Offer.date.between(
                current_datetime - timedelta(hours=24), current_datetime
            ))
        )).scalars()
        return dict(items=[tools.stat_to_response_dict(o, 'OFFER') for o in offers])
