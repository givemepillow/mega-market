from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from market.api import schemas
from market.api.handlers.exceptions import ValidationFailed400
from market.db.orm import Session
from market.db import model
from market.api.handlers import tools


def prepare(unit_import: schemas.ShopUnitImportRequest) -> (list, list, list, dict):
    """
    Подготовка данных для вставки/обновления: категории и товары
    разделяются на отдельные списки, создается общий список юнитов.
    Кроме того собирается словарь uuid-тип для того чтобы в функции handle,
    можно было проверить не изменяется ли тип уже существующего юнита.
    :raise ValidationFailed400: в случае невалидных данный выбрасывается исключение.
    """
    if not unit_import.items:
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
    print(f"{types=}")
    return categorise, offers, units, types


async def parents(units: list[dict], uuids: dict, session: Session) -> set[UUID]:
    """
    Находит все категории, которые необходимо обновить из-за вставки новых или
    изменения уже существующих данных прямо или косвенно влияющих
    на среднюю цену и дату родительских каталогов.
    :param uuids: словарь со всеми импортируемыми uuid.
    :param units: список словарей для вставки/обновления.
    :param session: сессия БД.
    :return: множество uuid всех категорий дата и средняя ценя которых подлежит обновлению.
    """
    updated_categories = set()
    import_categories = {u for u, t in uuids.items() if t == schemas.ShopUnitType.CATEGORY}
    # Добавление родительских категорий элементов импорта.
    all_parents = {unit['parent_id'] for unit in units}
    # Добавление родительских категорий элементов до импорта.
    all_parents |= set((await session.execute(
        select(model.ShopUnit.parent_id).
        where(model.ShopUnit.uuid.in_(uuids))
    )).scalars()) - {None}
    for parent_uuid in all_parents:
        while parent_uuid:
            # Если данный каталог уже в множестве, то не имеет смысла искать его предков.
            if parent_uuid in updated_categories:
                break
            updated_categories.add(parent_uuid)
            # Получаем следующую категорию верхнего уровня.
            parent_uuid = (await session.execute(
                select(model.Category.parent_id).
                where(model.Category.uuid == parent_uuid)
            )).scalar()
    updated_categories |= import_categories
    updated_categories.discard(None)
    return updated_categories


async def handle(unit_import: schemas.ShopUnitImportRequest):
    """
    Вставка и валидация данных, полученных от пользователя, в рамках одной транзакции.
    :raise ValidationFailed400: выбрасывает исключение, если данные невалидны.
    """
    categorise, offers, units, types = prepare(unit_import)
    async with Session() as s:
        async with s.begin():
            try:
                # Получаем типы юнитов, которые ВОЗМОЖНО будем обновлять.
                result = await s.execute(
                    select(model.ShopUnit).
                    where(model.ShopUnit.uuid.in_(types))
                )
                # Проверяем что не изменяется тип уже существующего юнита.
                for u, in result.all():
                    if u.type != types[u.uuid]:
                        raise ValidationFailed400("it is not allowed to change the unit type")
                # Вставка/обновление категорий.
                if categorise:
                    category_insert_stmt = insert(model.Category).values(categorise)
                    await s.execute(
                        category_insert_stmt.
                        on_conflict_do_update(
                            index_elements=['uuid'],
                            set_=category_insert_stmt.excluded
                        ))
                # Вставляем НОВЫЕ юниты. Вставка происходит ОБЯЗАТЕЛЬНО после категорий,
                # иначе каталога юнита может ЕЩЁ НЕ БЫТЬ в базе данных.
                unit_insert_stmt = insert(model.ShopUnit).values(units)
                await s.execute(
                    unit_insert_stmt.
                    on_conflict_do_update(
                        index_elements=['uuid'],
                        set_=unit_insert_stmt.excluded
                    ))
                # Вставка/обновление товаров.
                if offers:
                    offer_insert_stmt = insert(model.Offer).values(offers)
                    await s.execute(
                        offer_insert_stmt.
                        on_conflict_do_update(
                            index_elements=['uuid'],
                            set_=offer_insert_stmt.excluded
                        ))
                    await s.execute(insert(model.OffersHistory).values(offers))
                parent_uuids = await parents(units, uuids=types, session=s)
                updated_categories = (await s.execute(
                    select(model.Category).
                    where(model.Category.uuid.in_(parent_uuids))
                )).scalars()
                average_updates = []
                for p in updated_categories:
                    average_updates.append({
                        '_uuid': p.uuid,
                        'parent_id': p.parent_id,
                        'name': p.name,
                        'average_price': await tools.average_price(p, s),
                        'date': unit_import.update_date,
                    })
                if average_updates:
                    await tools.update_average_in_db(average_updates, s)
            except IntegrityError as err:
                raise ValidationFailed400(err)
