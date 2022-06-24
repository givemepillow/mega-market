from datetime import datetime
from typing import Optional, Dict, Union

from market.api import schemas
from market.api.handlers.exceptions import ValidationFailed400
from market.db import model


def avg(total: Optional[int], number: int) -> int:
    return int(total / number) if number else None


def iso8601(date: datetime) -> str:
    return date.isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def category_to_dict(category: model.Category) -> Dict:
    return dict(
        id=category.uuid,
        type=schemas.ShopUnitType.CATEGORY,
        name=category.name,
        parentId=category.parent_id,
        price=avg(category.total_price, category.offers_number),
        date=iso8601(category.date),
        children=[]
    )


def offer_to_dict(offer: model.Offer) -> Dict:
    return dict(
        id=offer.uuid,
        name=offer.name,
        parentId=offer.parent_id,
        type=schemas.ShopUnitType.OFFER,
        price=offer.price,
        date=iso8601(offer.date),
        children=None
    )


def category_row_to_dict(uuid, parent_id, name, date, total, number) -> Dict:
    return dict(
        id=uuid,
        type=schemas.ShopUnitType.CATEGORY,
        name=name,
        parentId=parent_id,
        price=avg(total, number),
        date=iso8601(date),
        children=[]
    )


def offer_row_to_dict(uuid, parent_id, name, date, price) -> Dict:
    return dict(
        id=uuid,
        type=schemas.ShopUnitType.OFFER,
        name=name,
        parentId=parent_id,
        price=price,
        date=iso8601(date),
        children=None
    )


def unit_price(m: Union[model.Category, model.Base], unit_type: str) -> Optional[int]:
    if unit_type == schemas.ShopUnitType.OFFER:
        return m.price
    return avg(m.total_price, m.offers_number)


def stat_to_response_dict(m: Union[model.Category, model.Base], unit_type: str) -> Dict:
    return dict(
        id=m.uuid,
        name=m.name,
        parentId=m.parent_id,
        type=unit_type,
        price=unit_price(m, unit_type),
        date=iso8601(m.date)
    )


def to_datetime(string: str) -> datetime:
    """
    Конвертация строки с датой и временем в объект datetime.
    :raise ValidationFailed400: выбрасывает исключение если дата не соответствует ISO 8601.
    """
    try:
        return datetime.fromisoformat(string.replace('Z', '+00:00'))
    except ValueError:
        raise ValidationFailed400(f'incorrect date format "{string}"')
