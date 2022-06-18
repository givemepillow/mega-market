from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from market.api import schemas
from market.api.handlers.exceptions import ValidationFailed400
from market.db.orm import Session
from market.db import model


def prepare(unit_import: schemas.ShopUnitImportRequest) -> (list, list, list, dict):
    """
    Подготовка данных для вставки/обновления: категории и товары
    разделяются на отдельные списки, создается общий список юнитов.
    Кроме того собирается словарь uuid-тип для того чтобы в функции handle,
    можно было проверить не изменяется ли тип уже существующего юнита.
    :raise ValidationFailed400: в случае не валидных данный выбрасывается исключение.
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
    return categorise, offers, units, types


async def handle(unit_import: schemas.ShopUnitImportRequest):
    """
    Вставка и валидация данных, полученных от пользователя, в рамках одной транзакции.
    :raise ValidationFailed400:
    :param unit_import:
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
                    await s.execute(insert(model.CategoryHistory).values(categorise))
                # Вставляем НОВЫЕ юниты.
                # Вставка происходит ОБЯЗАТЕЛЬНО после категорий, иначе каталога юнита может
                # ЕЩЁ НЕ БЫТЬ в базе данных в момент вставки его содержимого.
                # (в случае, если в одной транзакции вставляются категории и их содержимое)
                await s.execute(
                    insert(model.ShopUnit).
                    values(units).
                    on_conflict_do_nothing(index_elements=['uuid'])  # Уже существующее не трогается.
                )
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
                # Исключения типа IntegrityError (или его наследники) возникают при ошибке целостности,
                # а это означает, что данные пользователя невалидны.
            except (IntegrityError, ValidationFailed400) as err:
                raise ValidationFailed400(err)
