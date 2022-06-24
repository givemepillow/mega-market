from datetime import datetime
from typing import List, Dict, Set, Tuple
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from market.api import schemas
from market.api.handlers.exceptions import ValidationFailed400
from market.db.orm import Session
from market.db import crud

MAX_ITEMS = 6500


def prepare(unit_import: schemas.ShopUnitImportRequest) -> Tuple[List, List, List, Dict]:
    """
    Подготовка данных для вставки/обновления: категории и товары
    разделяются на отдельные списки, создается общий список юнитов.
    Кроме того собирается словарь uuid-тип для того чтобы в функции handle,
    можно было проверить не изменяется ли тип уже существующего юнита.
    :raise ValidationFailed400: в случае невалидных данный выбрасывается исключение.
    """
    print("quantity: ", len(unit_import.items))
    if len(unit_import.items) > MAX_ITEMS:
        raise ValidationFailed400(f"to many items: {len(unit_import.items)}")
    elif not unit_import.items:
        raise ValidationFailed400("empty list of units")
    categorise, offers, units, types = [], [], [], {}
    for unit in unit_import.items:
        # Проверка уникальности uuid в рамках запроса.
        if unit.id in types:
            raise ValidationFailed400("duplicate uuid in a single request")
        types[unit.id] = unit.type
        if unit.type == 'CATEGORY':
            # Проверка, что у категории отсутствует цена.
            if unit.price is not None:
                raise ValidationFailed400("unit with the CATEGORY type cannot contain  a price field")
            categorise.append({
                'uuid': unit.id,
                'parent_id': unit.parent_id,
                'name': unit.name,
                'date': unit_import.update_date
            })
        elif unit.type == 'OFFER':
            # Проверка, что у товара присутствует цена.
            if unit.price is None:
                raise ValidationFailed400("unit with the OFFER type must contain a price field")
            offers.append({
                'uuid': unit.id,
                'parent_id': unit.parent_id,
                'name': unit.name,
                'date': unit_import.update_date,
                'price': unit.price
            })
        units.append({'uuid': unit.id, 'type': unit.type, 'parent_id': unit.parent_id})
    return categorise, offers, units, types


async def parents(units: List[Dict], uuids: Dict, session: Session) -> Set[UUID]:
    """
    Находит все категории, которые необходимо обновить из-за вставки новых или
    изменения уже существующих данных прямо или косвенно влияющих
    на среднюю цену и дату родительских каталогов.
    :param uuids: словарь со всеми импортируемыми uuid.
    :param units: список словарей для вставки/обновления.
    :param session: сессия БД.
    :return: множество uuid всех категорий дата и средняя ценя которых подлежит обновлению.
    """
    categories_to_update = {u for u, t in uuids.items() if t == schemas.ShopUnitType.CATEGORY}
    # Добавление родительских категорий элементов импорта.
    _parents = {unit['parent_id'] for unit in units}
    # Добавление родительских категорий элементов до импорта.
    _parents.update(u.parent_id for u in await crud.ShopUnit.get_by_uuids(uuids, session))
    _parents.discard(None)
    if _parents:
        ancestors = await crud.Category.get_ancestors(_parents, session)
        categories_to_update.update(ancestors)
    categories_to_update.discard(None)
    return categories_to_update


async def handle(unit_import: schemas.ShopUnitImportRequest):
    """
    Вставка и валидация данных, полученных от пользователя, в рамках одной транзакции.
    :raise ValidationFailed400: выбрасывает исключение, если данные невалидны.
    """
    categorise, offers, units, types = prepare(unit_import)
    async with Session() as s:
        async with s.begin():
            start_time = datetime.now()
            try:
                parents_uuids = await parents(units, uuids=types, session=s)
                # Проверяем что не изменяется тип уже существующего юнита.
                for u in (await crud.ShopUnit.get_by_uuids(types, s)):
                    if u.type != types[u.uuid]:
                        raise ValidationFailed400("it is not allowed to change the unit type")
                # Вставка/обновление категорий.
                if categorise:
                    await crud.Category.save_or_update(categorise, s)
                # Вставляем НОВЫЕ юниты. Вставка происходит ОБЯЗАТЕЛЬНО после категорий,
                # иначе каталога юнита может ЕЩЁ НЕ БЫТЬ в базе данных.
                await crud.ShopUnit.save_or_update(units, s)
                # Вставка/обновление товаров.
                if offers:
                    await crud.Offer.save_or_update(offers, s)
                if parents_uuids:
                    await crud.Category.update_statistics(parents_uuids, unit_import.update_date, s)
                    await crud.History.add_from_categories(parents_uuids, s)
                print("import time: ", datetime.now() - start_time)
            except IntegrityError:
                raise ValidationFailed400("db integrity error")
