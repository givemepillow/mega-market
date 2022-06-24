from datetime import datetime, timedelta
from typing import Optional, List, Iterable
from uuid import UUID

from sqlalchemy import select, delete, and_, text, desc, bindparam
from sqlalchemy.dialects.postgresql import insert

from market.api import schemas
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
    async def delete(uuid: UUID, session: Session) -> schemas.ShopUnitType:
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


class Category:
    @staticmethod
    async def delete(uuid: UUID, session: Session):
        (parent_uuid, deleted_total, deleted_number), = (await session.execute(
            delete(model.Category).
            where(and_(
                model.Category.uuid == uuid
            )).returning(
                model.Category.parent_id,
                model.Category.total_price,
                model.Category.offers_number
            )
        )).all()
        return parent_uuid, deleted_total, deleted_number

    @staticmethod
    async def update_after_delete(
            parent_uuid: UUID,
            deleted_total: int,
            deleted_number: int,
            session: Session

    ) -> Iterable[UUID]:
        stmt = text(
            """
            with recursive r as (
                select uuid, parent_id
                from categories
                where uuid = :uuid
                UNION
                select c.uuid, c.parent_id
                from r
                join categories c on c.uuid = r.parent_id
            ) update categories
              set total_price = total_price - :deleted_total,
                  offers_number = offers_number - :deleted_number
              where uuid in (select uuid from r)
              returning categories.uuid;
            """
        )
        return (await (session.execute(stmt, {
            'uuid': parent_uuid,
            'deleted_total': deleted_total,
            'deleted_number': deleted_number
        }))).scalars()

    @staticmethod
    async def get_ancestors(uuids: Iterable[UUID], session: Session):
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
        # Получаем всех предков вплоть до корня.
        return (await session.execute(
            stmt.bindparams(bindparam('uuids', expanding=True)),
            {'uuids': tuple(uuids)}
        )).scalars()

    @staticmethod
    async def save_or_update(categories: List[dict], session: Session):
        category_insert_stmt = insert(model.Category).values(categories)
        await session.execute(
            category_insert_stmt.
            on_conflict_do_update(
                index_elements=['uuid'],
                set_=category_insert_stmt.excluded
            ))

    @staticmethod
    async def update_statistics(uuids, update_date: datetime, session: Session):
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
                    select r.root, sum(o.price) as sum , count(o.uuid) as count from r
                    left join offers o on r.current_uuid = o.parent_id
                    group by r.root
                ) as recursive where c.uuid = recursive.root;
            """
        )
        await session.execute(stmt.bindparams(
            bindparam('uuids', expanding=True)),
            {'uuids': tuple(uuids), 'date': update_date}
        )


class Offer:
    @staticmethod
    async def delete(uuid: UUID, session: Session):
        (parent_uuid, deleted_total), = (await session.execute(
            delete(model.Offer).
            where(and_(
                model.Offer.uuid == uuid
            )).returning(
                model.Offer.parent_id,
                model.Offer.price
            )
        )).all()
        return parent_uuid, deleted_total

    async def get(uuid: UUID, session: Session):
        return (await session.execute(
            select(model.Offer).
            where(model.Offer.uuid == uuid)
        )).scalar()

    async def get_for_24_hours(current_datetime: datetime, session: Session):
        return (await session.execute(
            select(model.Offer).
            where(model.Offer.date.between(
                current_datetime - timedelta(hours=24), current_datetime
            ))
        )).scalars()

    @staticmethod
    async def save_or_update(offers: List[dict], session: Session):
        offer_insert_stmt = insert(model.Offer).values(offers)
        await session.execute(
            offer_insert_stmt.
            on_conflict_do_update(
                index_elements=['uuid'],
                set_=offer_insert_stmt.excluded
            ))
        await session.execute(insert(model.OffersHistory).values(offers))


class History:
    @staticmethod
    def _statement(unit_model: model.Base, start: datetime, end: datetime):
        """
        Собирает запрос в зависимости от того присутствует ли время начала период
        и/или время окончания периода.
        """
        stmt = select(unit_model)
        if start and end:
            stmt = stmt.where(unit_model.date.between(start, end))
        elif start:
            stmt = stmt.where(unit_model.date >= start)
        elif end:
            stmt = stmt.where(unit_model.date <= end)
        return stmt

    @classmethod
    async def of_category_between_datetime(cls, uuid: UUID, start: datetime, end: datetime, session: Session):
        return (await session.execute(
            cls._statement(model.CategoryHistory, start, end).
            where(model.CategoryHistory.uuid == uuid).
            order_by(desc(model.CategoryHistory.date))
        )).scalars()

    @classmethod
    async def of_offers_between_datetime(cls, uuid: UUID, start: datetime, end: datetime, session: Session):
        return (await session.execute(
            cls._statement(model.OffersHistory, start, end).
            where(model.OffersHistory.uuid == uuid).
            order_by(desc(model.OffersHistory.date))
        )).scalars()

    @staticmethod
    async def add_from_categories(uuid_s: Iterable[UUID], session: Session):
        await session.execute(
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
                ).where(model.Category.uuid.in_(uuid_s))
            ))


async def get_nodes(uuid: UUID, session: Session):
    stmt = text(
        """
        with recursive r as (
            select 0 as level,uuid, null::uuid as parent_id, name, date, total_price, offers_number
            from categories
            where uuid = :uuid
            UNION ALL
            select r.level + 1, c.uuid, c.parent_id, c.name, c.date, c.total_price, c.offers_number
            from r
            join categories c on c.parent_id = r.uuid
        ) select 
            r.uuid, r.parent_id, r.name, r.date, r.total_price, r.offers_number,
            o.uuid, o.parent_id, o.name, o.date, o.price
          from r
            left join offers o on r.uuid = o.parent_id order by r.level, r.uuid=o.parent_id, o.date;
        """
    )
    return (await session.execute(stmt, {'uuid': str(uuid)})).all()
