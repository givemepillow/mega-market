from datetime import datetime
from uuid import UUID

from sqlalchemy import select, desc

from market.api.handlers.exceptions import ItemNotFound404
from market.db.orm import Session
from market.db import model
from market.api.schemas import ShopUnitType, ShopUnitStatisticResponse, ShopUnitStatisticUnit


def statement(unit_model: model.Base, start: datetime, end: datetime):
    """
    Собирает запрос в зависимости от того присутствует ли время начала период
    и/или время окончания периода.
    """
    stmt = select(unit_model)
    if start and end:
        stmt = stmt.where(unit_model.date.between(start, end))
    elif start:
        stmt = stmt.where(unit_model.date >= start)
    elif end:
        stmt = stmt.where(unit_model.date <= end)
    return stmt


async def handle(uuid: UUID, start: datetime, end: datetime):
    """
    Возвращает статистику изменений юнита за указанный период от - до.
    :raises ItemNotFound404 в случае если в БД не юнита с переданными uuid.
    """
    async with Session() as s:
        unit_type = (await s.execute(
            select(model.ShopUnit.type).
            where(model.ShopUnit.uuid == uuid)
        )).scalar()
        if not unit_type:
            raise ItemNotFound404(f'unit with uuid "{uuid}" does not exist')
        if datetime:
            if unit_type == ShopUnitType.CATEGORY:
                history = (await s.execute(
                    statement(model.CategoryHistory, start, end).
                    where(model.CategoryHistory.uuid == uuid).
                    order_by(desc(model.CategoryHistory.date))
                )).scalars()
            else:
                history = (await s.execute(
                    statement(model.OffersHistory, start, end).
                    where(model.OffersHistory.uuid == uuid).
                    order_by(desc(model.OffersHistory.date))
                )).scalars()
        return ShopUnitStatisticResponse(
            items=[ShopUnitStatisticUnit(
                id=u.uuid,
                name=u.name,
                parent_id=u.parent_id,
                type=unit_type,
                price=u.price if unit_type == ShopUnitType.OFFER else u.average_price,
                date=u.date
            ) for u in history]
        )
