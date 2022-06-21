from uuid import UUID

from sqlalchemy import delete, and_, select, update
from sqlalchemy.dialects.postgresql import insert

from market.db.orm import Session
from market.db import model
from market.api.handlers.exceptions import ItemNotFound404
from market.api import schemas


async def update_parents(first_parent_uuid: UUID, deleted_total: int, deleted_number: int, session: Session):
    update_uuids, updates = [], []
    parent = (await session.execute(
        select(model.Category).
        where(model.Category.uuid == first_parent_uuid)
    )).scalar()
    while parent:
        update_uuids.append(parent.uuid)
        updates.append({
            'uuid': parent.uuid,
            'total_price': parent.total_price - deleted_total,
            'offers_number': parent.offers_number - deleted_number,
            'date': parent.date,
            'parent_id': parent.parent_id,
            'name': parent.name
        })
        # Получаем следующую категорию верхнего уровня.
        parent = (await session.execute(
            select(model.Category).
            where(model.Category.uuid == parent.parent_id)
        )).scalar()
    await session.execute(
        update(model.Category).
        where(model.Category.uuid.in_(update_uuids)).
        values(
            total_price=model.Category.total_price - deleted_total,
            offers_number=model.Category.offers_number - deleted_number
        ))
    await session.execute(insert(model.CategoryHistory).values(updates))


async def handle(unit_uuid: UUID):
    """
    Удаление юнита по его uuid и обновление родительских категорий.
    :param unit_uuid: uuid юнита подлежащего удалению.
    """
    async with Session() as s:
        async with s.begin():
            # Получаем тип удаляемого юнита и удаляем его из таблицы с типами shop_units.
            # Удалять нужно обязательно т.к. каскадное удаление для shop_units
            # не сработает при удалении из товаров.
            unit_type = (await s.execute(
                delete(model.ShopUnit).
                where(model.ShopUnit.uuid == unit_uuid).
                returning(model.ShopUnit.type)
            )).scalar()
            # Если unit_type is None, то удаляемого юнита не существует.
            if not unit_type:
                raise ItemNotFound404(f'unit with uuid "{unit_uuid}" does not exist')
            # От типа удаляем категорию и её содержимое или товар.
            if unit_type == schemas.ShopUnitType.CATEGORY:
                # Каскадное удаление категорий.
                (parent_uuid, deleted_total, deleted_number), = (await s.execute(
                    delete(model.Category).
                    where(and_(
                        model.Category.uuid == unit_uuid
                    )).returning(
                        model.Category.parent_id,
                        model.Category.total_price,
                        model.Category.offers_number
                    )
                )).all()
            else:
                # Каскадное удаление товаров.
                (parent_uuid, deleted_total), = (await s.execute(
                    delete(model.Offer).
                    where(and_(
                        model.Offer.uuid == unit_uuid
                    )).returning(
                        model.Offer.parent_id,
                        model.Offer.price
                    )
                )).all()
                deleted_number = 1
            if not parent_uuid:
                return
            await update_parents(parent_uuid, deleted_total, deleted_number, s)
