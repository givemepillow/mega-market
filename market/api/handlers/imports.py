from datetime import datetime
from typing import List, Dict, Set, Tuple
from uuid import UUID

from sqlalchemy import select, bindparam, text, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from market.api import schemas
from market.api.handlers.exceptions import ValidationFailed400
from market.db.orm import Session
from market.db import model, crud

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
                'date': unit_import.update_date,
                'total_price': 0,
                'offers_number': 0
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
    _parents.update((await session.execute(
        select(model.ShopUnit.parent_id).
        where(model.ShopUnit.uuid.in_(uuids))
    )).scalars())
    _parents.discard(None)

    stmt = text(
        """
        with recursive r as (
            select uuid
            from categories
            where uuid in :uuids
            UNION DISTINCT
            select c.parent_id
            from r
            join categories c on c.uuid = r.uuid
        ) select uuid from r;
        """
    )

    if _parents:
        # Получаем всех предков вплоть до корня.
        ancestors = (await session.execute(
            stmt.bindparams(bindparam('uuids', expanding=True)),
            {'uuids': tuple(_parents)}
        )).scalars()
        categories_to_update.update(ancestors)

    categories_to_update.discard(None)
    return categories_to_update


async def insert_imported_units(
        categorise: List[dict],
        offers: List[dict],
        units: List[dict],
        types: Dict,
        session: Session
):
    # Проверяем что не изменяется тип уже существующего юнита.
    for u in (await crud.ShopUnit.get_by_uuids(types, session)):
        if u.type != types[u.uuid]:
            raise ValidationFailed400("it is not allowed to change the unit type")
    # Вставка/обновление категорий.
    if categorise:
        category_insert_stmt = insert(model.Category).values(categorise)
        await session.execute(
            category_insert_stmt.
            on_conflict_do_update(
                index_elements=['uuid'],
                set_=category_insert_stmt.excluded
            ))
    # Вставляем НОВЫЕ юниты. Вставка происходит ОБЯЗАТЕЛЬНО после категорий,
    # иначе каталога юнита может ЕЩЁ НЕ БЫТЬ в базе данных.
    unit_insert_stmt = insert(model.ShopUnit).values(units)
    await session.execute(
        unit_insert_stmt.
        on_conflict_do_update(
            index_elements=['uuid'],
            set_=unit_insert_stmt.excluded
        ))
    # Вставка/обновление товаров.
    if offers:
        offer_insert_stmt = insert(model.Offer).values(offers)
        await session.execute(
            offer_insert_stmt.
            on_conflict_do_update(
                index_elements=['uuid'],
                set_=offer_insert_stmt.excluded
            ))
        await session.execute(insert(model.OffersHistory).values(offers))


async def handle(unit_import: schemas.ShopUnitImportRequest):
    """
    Вставка и валидация данных, полученных от пользователя, в рамках одной транзакции.
    :raise ValidationFailed400: выбрасывает исключение, если данные невалидны.
    """
    categorise, offers, units, types = prepare(unit_import)
    async with Session() as s:
        async with s.begin():
            try:
                start = datetime.now()
                parent_uuids = await parents(units, uuids=types, session=s)
                await insert_imported_units(categorise, offers, units, types, s)
                if not parent_uuids:
                    return
                stmt = text(
                    """
                    with recursive r as (
                        select uuid as root, uuid as current_uuid
                        from categories
                        where uuid in :uuids
                        UNION
                        select r.root, c.uuid
                        from r
                        join categories c on c.parent_id = r.current_uuid
                    ) update categories c
                        set total_price = recursive.sum, offers_number = recursive.count,
                        date = :date
                        from (
                            select r.root, sum(o.price)::INT as sum , count(o.uuid) as count from r
                            left join offers o on r.current_uuid = o.parent_id
                            group by r.root
                        ) as recursive where c.uuid = recursive.root
                        returning c.uuid;
                    """
                )
                updated = (await s.execute(stmt.bindparams(
                    bindparam('uuids', expanding=True)),
                    {'uuids': tuple(parent_uuids), 'date': unit_import.update_date}
                )).scalars()
                await s.execute(
                    insert(model.CategoryHistory).
                    from_select(
                        ['uuid', 'parent_id', 'date', 'name', 'total_price', 'offers_number'],
                        select(
                            model.Category.uuid,
                            model.Category.parent_id,
                            model.Category.date,
                            model.Category.name,
                            model.Category.total_price,
                            model.Category.offers_number
                        ).where(model.Category.uuid.in_(parent_uuids))
                    ))
                print("imports time: ", datetime.now() - start)
            except IntegrityError:
                raise ValidationFailed400("db integrity error")
