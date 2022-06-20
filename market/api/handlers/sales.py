from datetime import datetime, timedelta

from sqlalchemy import select

from market.db.orm import Session
from market.db import model
from market.api.schemas import ShopUnitStatisticResponse, ShopUnitStatisticUnit, ShopUnitType


async def handle(current_datetime: datetime) -> ShopUnitStatisticResponse:
    """
    Возвращает товары, цена которых была обновлена за 24 ч до переданной даты.
    """
    async with Session() as s:
        offers = (await s.execute(
            select(model.Offer).
            where(model.Offer.date.between(
                current_datetime - timedelta(hours=24), current_datetime
            ))
        )).scalars()
        return ShopUnitStatisticResponse(
            items=[ShopUnitStatisticUnit(
                id=o.uuid,
                name=o.name,
                parent_id=o.parent_id,
                type=ShopUnitType.OFFER,
                price=o.price,
                date=o.date
            ) for o in offers]
        )
