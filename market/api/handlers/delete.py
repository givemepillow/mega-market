from uuid import UUID

from sqlalchemy import delete, and_, text

from market.db.orm import Session
from market.db import model, crud
from market.api.handlers.exceptions import ItemNotFound404
from market.api import schemas


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
            unit_type = await crud.ShopUnit.delete(unit_uuid, s)
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
            stmt = text(
                """
                with recursive r as (
                    select uuid, parent_id
                    from categories
                    where uuid = :_uuid
                    UNION
                    select c.uuid, c.parent_id
                    from r
                    join categories c on c.uuid = r.parent_id
                ) update categories
                  set total_price = total_price - :deleted_total,
                      offers_number = offers_number - :deleted_number
                  where uuid in (select uuid from r);
                """
            )
            await (s.execute(stmt, {
                '_uuid': parent_uuid,
                'deleted_total': deleted_total,
                'deleted_number': deleted_number
            }))
