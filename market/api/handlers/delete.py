from uuid import UUID

from sqlalchemy import delete, and_, select
from sqlalchemy.exc import IntegrityError

from market.db.orm import Session
from market.db import model
from market.api.handlers.exceptions import ItemNotFound404, ValidationFailed400
from market.api import schemas
from market.api.handlers import tools


async def update(parent_uuid: UUID, session: Session):
    """
    Обновляет данные каталогов после удаления юнита из базы данных.
    """
    try:
        average_updates = []
        parent = (await session.execute(
            select(model.Category).
            where(model.Category.uuid == parent_uuid)
        )).scalar()
        while parent:
            average_updates.append({
                '_uuid': parent.uuid,
                'average_price': await tools.average_price(parent, session),
                'date': parent.date,
                'parent_id': parent.parent_id,
                'name': parent.name
            })
            # Получаем следующую категорию верхнего уровня.
            parent = (await session.execute(
                select(model.Category).
                where(model.Category.uuid == parent.parent_id)
            )).scalar()
        await tools.update_average_in_db(average_updates, session)
    except IntegrityError as e:
        raise ValidationFailed400(e)


async def handle(unit_uuid: UUID):
    """
    Удаление юнита по его uuid.
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
                parent_uuid = (await s.execute(
                    delete(model.Category).
                    where(and_(
                        model.Category.uuid == unit_uuid
                    )).returning(model.Category.parent_id)
                )).scalar()
            else:
                # Каскадное удаление товаров.
                parent_uuid = (await s.execute(
                    delete(model.Offer).
                    where(and_(
                        model.Offer.uuid == unit_uuid
                    )).returning(model.Offer.parent_id)
                )).scalar()
            if not parent_uuid:
                return
            await update(parent_uuid, session=s)
