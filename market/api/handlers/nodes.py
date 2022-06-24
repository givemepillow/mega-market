from datetime import datetime
from typing import Dict
from uuid import UUID

from sqlalchemy import select

from market.db.orm import Session
from market.db import model, crud
from market.api import schemas
from market.api.handlers import exceptions, tools


async def sub(category_uuid: UUID, session: Session) -> (Dict, Dict):
    """
    Извлекает товары и подкатегории каталога собирает из них списки словарей.
    :return: список полученных категорий.
    """
    subcategories = (await session.execute(
        select(model.Category).
        where(model.Category.parent_id == category_uuid)
    )).scalars()
    node_categories = [tools.category_to_response_dict(c) for c in subcategories]
    offers = (await session.execute(
        select(model.Offer).
        where(model.Offer.parent_id == category_uuid)
    )).scalars()
    node_offers = [tools.offer_to_response_dict(o) for o in offers]
    return node_offers, node_categories


async def handle(unit_uuid: UUID) -> Dict:
    async with Session() as s:
        async with s.begin():
            start_time = datetime.now()
            unit = await crud.ShopUnit.get(unit_uuid, s)
            if unit is None:
                raise exceptions.ItemNotFound404(f'unit with "{unit_uuid}" does not exist')
            if unit.type == schemas.ShopUnitType.OFFER:
                offer = (await s.execute(
                    select(model.Offer).
                    where(model.Offer.uuid == unit_uuid)
                )).scalar()
                return tools.offer_to_response_dict(offer)
            else:
                category = (await s.execute(
                    select(model.Category).
                    where(model.Category.uuid == unit_uuid)
                )).scalar()
                root = tools.category_to_response_dict(category)
                # Обход дерева категорий через стек.
                stack = [(category.uuid, root)]
                while stack:
                    uuid, parent = stack.pop()
                    offers, categories = await sub(uuid, s)
                    parent['children'] = offers + categories
                    parent['children'].sort(key=lambda x: x['date'], reverse=True)
                    for c in categories:
                        stack.append((c.get('id'), c))
                print(f"tree extract time: {datetime.now() - start_time}")
                return root
