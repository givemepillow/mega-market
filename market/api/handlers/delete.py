from uuid import UUID

from market.db.orm import Session
from market.db import crud
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
            elif unit_type == schemas.ShopUnitType.CATEGORY:
                parent_uuid, deleted_total, deleted_number = await crud.Category.delete(unit_uuid, s)
            else:
                parent_uuid, deleted_total = await crud.Offer.delete(unit_uuid, s)
                deleted_number = 1
            if parent_uuid:
                # Обновляем данные все родителей удалённого юнита.
                updated = await crud.Category.update_after_delete(parent_uuid, deleted_total, deleted_number, s)
                if updated:
                    # Сохраняем в историю.
                    await crud.History.add_from_categories(updated, s)
