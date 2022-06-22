from typing import Optional, List, Iterable
from uuid import UUID

from sqlalchemy import select, delete, and_
from sqlalchemy.dialects.postgresql import insert

from market.db import model
from market.db.orm import Session


class ShopUnit:
    @staticmethod
    async def save_or_update(units: List[dict], session: Session):
        unit_insert_stmt = insert(model.ShopUnit).values(units)
        await session.execute(
            unit_insert_stmt.
            on_conflict_do_update(
                index_elements=['uuid'],
                set_=unit_insert_stmt.excluded
            ))

    @staticmethod
    async def get(uuid: UUID, session: Session) -> Optional[model.ShopUnit]:
        return (await session.execute(
            select(model.ShopUnit).
            where(model.ShopUnit.uuid == uuid))).scalar()

    @staticmethod
    async def get_by_uuids(uuids: Iterable[UUID], session: Session) -> List[model.ShopUnit]:
        return (await session.execute(
            select(model.ShopUnit).
            where(model.ShopUnit.uuid.in_(uuids))
        )).scalars()

    @staticmethod
    async def delete(uuid: UUID, session: Session) -> (str, UUID):
        return (await session.execute(
            delete(model.ShopUnit).
            where(model.ShopUnit.uuid == uuid).
            returning(model.ShopUnit.type)
        )).scalar()

    @staticmethod
    async def get_parent_uuids_by_uuids(uuids: Iterable[UUID], session: Session):
        return (await session.execute(
            select(model.ShopUnit.parent_id).
            where(and_(model.ShopUnit.uuid.in_(uuids), model.ShopUnit.parent_id.is_not(None)))
        )).scalars()
