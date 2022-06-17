from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from market.api import schemas
from market.api.handlers.exceptions import ValidationFailed400
from market.db.orm import Session
from market.db import model


def prepare(unit_import: schemas.ShopUnitImportRequest):
    """
    :raise ValidationFailed400:
    :param unit_import:
    """
    if not unit_import.items:
        raise ValidationFailed400("empty list of units")
    categorise, offers, units, types = [], [], [], {}
    for unit in unit_import.items:
        if unit.id in types:
            raise ValidationFailed400("duplicate uuid in a single request")
        types[unit.id] = unit.type
        if unit.type == 'CATEGORY':
            if unit.price is not None:
                raise ValidationFailed400("unit with the CATEGORY type cannot contain  a price field")
            categorise.append({
                'uuid': unit.id,
                'parent_id': unit.parent_id,
                'name': unit.name,
                'date': unit_import.update_date
            })
        elif unit.type == 'OFFER':
            if unit.price is None:
                raise ValidationFailed400("unit with the OFFER type must contain a price field")
            offers.append({
                'uuid': unit.id,
                'parent_id': unit.parent_id,
                'name': unit.name,
                'date': unit_import.update_date,
                'price': unit.price
            })
        units.append({'uuid': unit.id, 'type': unit.type})
    return categorise, offers, units, types


async def handle(unit_import: schemas.ShopUnitImportRequest):
    """
    :raise ValidationFailed400:
    :param unit_import:
    """
    categorise, offers, units, types = prepare(unit_import)
    async with Session() as s:
        async with s.begin():
            try:
                result = await s.execute(
                    select(model.ShopUnit).
                    where(model.ShopUnit.uuid.in_(types))
                )
                for u, in result.all():
                    if u.type != types[u.uuid]:
                        raise ValidationFailed400("it is not allowed to change the unit type")
                await s.execute(
                    insert(model.ShopUnit).
                    values(units).
                    on_conflict_do_nothing(index_elements=['uuid'])
                )
                if categorise:
                    category_insert_stmt = insert(model.Category).values(categorise)
                    await s.execute(
                        category_insert_stmt.
                        on_conflict_do_update(
                            index_elements=['uuid'],
                            set_=category_insert_stmt.excluded
                        ))
                    await s.execute(insert(model.CategoryHistory).values(categorise))
                if offers:
                    offer_insert_stmt = insert(model.Offer).values(offers)
                    await s.execute(
                        offer_insert_stmt.
                        on_conflict_do_update(
                            index_elements=['uuid'],
                            set_=offer_insert_stmt.excluded
                        ))
                    await s.execute(insert(model.OffersHistory).values(offers))
            except (IntegrityError, ValidationFailed400) as err:
                raise ValidationFailed400(err)
