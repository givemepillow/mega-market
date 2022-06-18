from uuid import UUID

from sqlalchemy import delete, and_, select

from market.db.orm import Session
from market.db import model
from market.api.handlers.exceptions import ItemNotFound404
from market.api import schemas


async def handle(unit_uuid: UUID):
    """
    Удаление юнита по его uuid.
    :param unit_uuid: uuid юнита подлежащего удалению.
    """
    async with Session() as s:
        async with s.begin() as transaction:
            # Получаем тип удаляемого юнита и удаляем его из таблицы с типами shop_units.
            # Удалять нужно обязательно т.к. каскадное удаление для shop_units
            # не сработает при удалении из товаров.
            result = await s.execute(
                delete(model.ShopUnit).
                where(model.ShopUnit.uuid == unit_uuid).
                returning(model.ShopUnit.type)
            )
            unit_type = result.scalar()
            # Если unit_type is None, то удаляемого юнита не существует.
            if not unit_type:
                raise ItemNotFound404(f"unit with uuid {unit_uuid} does not exist")
            else:
                # От типа удаляем категорию и её содержимое или товар.
                if unit_type == schemas.ShopUnitType.CATEGORY:
                    # Каскадное удаление категорий.
                    await s.execute(
                        delete(model.Category).
                        where(and_(
                            model.Category.uuid == unit_uuid
                        ))
                    )
                else:
                    # Каскадное удаление товаров.
                    await s.execute(
                        delete(model.Offer).
                        where(and_(
                            model.Offer.uuid == unit_uuid
                        ))
                    )
            await transaction.commit()
