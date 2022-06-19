from uuid import UUID

from sqlalchemy import select

from market.db.orm import Session
from market.db import model
from market.api import schemas
from market.api.handlers import exceptions


async def sub(category_uuid: UUID, node: schemas.ShopUnit, session: Session) -> [schemas.ShopUnit]:
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
        node_categories.append(schemas.ShopUnit(
            id=c.uuid,
            type=schemas.ShopUnitType.CATEGORY,
            name=c.name,
            parent_id=c.parent_id,
            price=c.average_price,
            date=c.date,
            children=[]
        ))
    offers = (await session.execute(
        select(model.Offer).
        where(model.Offer.parent_id == category_uuid)
    )).scalars()
    for o in offers:
        node_offers.append(schemas.ShopUnit(
            id=o.uuid,
            type=schemas.ShopUnitType.OFFER,
            name=o.name,
            parent_id=o.parent_id,
            price=o.price,
            date=o.date,
        ))
    node.children = node_offers + node_categories
    node.children.sort(key=lambda unit: unit.date, reverse=True)
    return node_categories


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
                return schemas.ShopUnit(
                    id=offer.uuid,
                    type=schemas.ShopUnitType.OFFER,
                    name=offer.name,
                    parent_id=offer.parent_id,
                    price=offer.price,
                    date=offer.date
                )
            else:
                category = (await s.execute(
                    select(model.Category).
                    where(model.Category.uuid == unit_uuid)
                )).scalar()
                root = schemas.ShopUnit(
                    id=category.uuid,
                    type=schemas.ShopUnitType.CATEGORY,
                    name=category.name,
                    parent_id=category.parent_id,
                    price=category.average_price,
                    date=category.date,
                    children=[]
                )
                # Обход дерева категорий через стек.
                # Стек используется чтобы не упереться в потолок рекурсивных вызовов.
                stack = [(category.uuid, root)]
                while stack:
                    uuid, node = stack.pop()
                    categories = await sub(uuid, node, s)
                    for c in categories:
                        stack.append((c.id, c))
                return root
