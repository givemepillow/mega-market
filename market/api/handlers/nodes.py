from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from sqlalchemy import select

from market.db.orm import Session
from market.db import model
from market.api import schemas
from market.api.handlers import exceptions


def iso8601(date: datetime) -> str:
    return date.isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def str_uuid_or_none(uuid: Optional[str]) -> Optional[str]:
    return str(uuid) if uuid else None


async def sub(category_uuid: UUID, session: Session) -> Dict:
    """
    Извлекает товары и подкатегории каталога собирает из них Pydantic-модели
    и присоединяет к родительской Pydantic-модели.
    :return: список полученных категорий.
    """
    node_offers, node_categories = [], []
    subcategories = (await session.execute(
        select(model.Category).
        where(model.Category.parent_id == category_uuid)
    )).scalars()
    for c in subcategories:
        node_categories.append(dict(
            id=str(c.uuid),
            type='CATEGORY',
            name=c.name,
            parentId=str_uuid_or_none(c.parent_id),
            price=c.average_price,
            date=iso8601(c.date),
            children=[]
        ))
    offers = (await session.execute(
        select(model.Offer).
        where(model.Offer.parent_id == category_uuid)
    )).scalars()
    for o in offers:
        node_offers.append(dict(
            id=str(o.uuid),
            type='OFFER',
            name=o.name,
            parentId=str_uuid_or_none(o.parent_id),
            price=o.price,
            date=iso8601(o.date),
            children=None
        ))
    return node_offers, node_categories


async def handle(unit_uuid: UUID) -> schemas.ShopUnit:
    async with Session() as s:
        async with s.begin():
            unit_type = (await s.execute(
                select(model.ShopUnit.type).
                where(model.ShopUnit.uuid == unit_uuid))).scalar()
            if unit_type is None:
                raise exceptions.ItemNotFound404(f'unit with "{unit_uuid}" does not exist')
            if unit_type == schemas.ShopUnitType.OFFER:
                offer = (await s.execute(
                    select(model.Offer).
                    where(model.Offer.uuid == unit_uuid)
                )).scalar()
                return dict(
                    id=str(offer.uuid),
                    type='OFFER',
                    name=offer.name,
                    parent_id=str_uuid_or_none(offer.parent_id),
                    price=offer.price,
                    date=iso8601(offer.date)
                )
            else:
                category = (await s.execute(
                    select(model.Category).
                    where(model.Category.uuid == unit_uuid)
                )).scalar()
                root = dict(
                    id=str(category.uuid),
                    type='CATEGORY',
                    name=category.name,
                    parentId=str_uuid_or_none(category.parent_id),
                    price=category.average_price,
                    date=iso8601(category.date),
                    children=[]
                )
                # Обход дерева категорий через стек.
                stack = [(category.uuid, root)]
                while stack:
                    uuid, parent = stack.pop()
                    offers, categories = await sub(uuid, s)
                    parent['children'] = offers + categories
                    parent['children'].sort(key=lambda x: x['date'], reverse=True)
                    for c in categories:
                        stack.append((c.get('id'), c))
                return root
