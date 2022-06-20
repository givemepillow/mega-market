from datetime import datetime
from typing import Optional, Dict

from sqlalchemy import select, bindparam, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from market.api.handlers.exceptions import ValidationFailed400
from market.db import model


def to_datetime(string: str) -> datetime:
    """
    Конвертация строки с датой и временем в объект datetime.
    :raise ValidationFailed400: выбрасывает исключение если дата не соответствует ISO 8601.
    """
    try:
        return datetime.fromisoformat(string.replace('Z', '+00:00'))
    except ValueError:
        raise ValidationFailed400(f'incorrect date format "{string}"')


async def average_price(category: model.Category, session: Session) -> Optional[int]:
    """
    Подсчитывает среднюю цену товара для каждой категории.
    Используется в handlers.imports и handlers.delete.
    :param category: категория для которой будет произведён подсчёт.
    :param session: сессия БД.
    :return: средняя стоимость товаров категории.
    """
    price_sum, count = 0, 0
    stack = [category]
    while stack:
        current_category = stack.pop()
        # Добавляем в стек подкатегории.
        stack += (await session.execute(
            select(model.Category).where(model.Category.parent_id == current_category.uuid)
        )).scalars() or []
        # Товары текущей категории.
        offers = (await session.execute(
            select(model.Offer.price).where(model.Offer.parent_id == current_category.uuid)
        )).scalars() or []
        for p in offers:
            price_sum += p
            count += 1
    return int(price_sum / count) if count else None


async def update_average_in_db(update_data: Dict, session: Session):
    """
    Вставляет и обновления данные обновлённых категорий из словаря.
    Используется в handlers.imports и handlers.delete.
    """
    await session.execute(insert(model.CategoryHistory).values(
        uuid=bindparam('_uuid'),
        average_price=bindparam('average_price'),
        date=bindparam('date'),
        parent_id=bindparam('parent_id'),
        name=bindparam('name')
    ), update_data)
    await session.execute(
        update(model.Category).
        where(model.Category.uuid == bindparam('_uuid')).
        values(date=bindparam('date'), average_price=bindparam('average_price')),
        update_data
    )
