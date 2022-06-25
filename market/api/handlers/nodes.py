from typing import Dict
from uuid import UUID

from market.db.orm import Session
from market.db import crud
from market.api import schemas
from market.api.handlers import exceptions, tools


async def handle(unit_uuid: UUID) -> Dict:
    async with Session() as s:
        async with s.begin():
            unit = await crud.ShopUnit.get(unit_uuid, s)
            if unit is None:
                raise exceptions.ItemNotFound404(f'unit with "{unit_uuid}" does not exist')
            if unit.type == schemas.ShopUnitType.OFFER:
                result = tools.offer_to_dict(await crud.Offer.get(unit_uuid, s))
                return result
            else:
                nodes = {}
                for line in await crud.get_nodes(unit_uuid, s):
                    c_u, c_parent, c_nm, c_dt, c_tm, c_num, o_u, o_parent, o_nm, o_dt, o_pr = line
                    if c_u not in nodes:
                        nodes[c_u] = tools.category_row_to_dict(c_u, c_parent, c_nm, c_dt, c_tm, c_num)
                        if c_parent:
                            nodes[c_parent]['children'].append(nodes[c_u])
                    if o_u:
                        nodes[c_u]['children'].append(tools.offer_row_to_dict(o_u, o_parent, o_nm, o_dt, o_pr))
                return nodes[unit_uuid]
