from datetime import datetime
from typing import Dict
from uuid import UUID

from market.db.orm import Session
from market.db import crud
from market.api import schemas
from market.api.handlers import exceptions, tools


async def handle(unit_uuid: UUID) -> Dict:
    async with Session() as s:
        async with s.begin():
            start_time = datetime.now()
            unit = await crud.ShopUnit.get(unit_uuid, s)
            if unit is None:
                raise exceptions.ItemNotFound404(f'unit with "{unit_uuid}" does not exist')
            if unit.type == schemas.ShopUnitType.OFFER:
                result = tools.offer_to_dict(await crud.Offer.get(unit_uuid, s))
                print("node returning time: ", datetime.now() - start_time)
                return result
            else:
                nodes = {}
                for line in await crud.get_nodes(unit_uuid, s):
                    c_uuid, c_parent_id, c_name, c_date, c_total, c_number, *offer = line
                    o_uuid, o_parent_id, o_name, o_date, o_price = offer
                    if c_uuid not in nodes:
                        nodes[c_uuid] = tools.category_row_to_dict(
                            c_uuid, c_parent_id, c_name, c_date, c_total, c_number
                        )
                        if c_parent_id:
                            nodes[c_parent_id]['children'].append(nodes[c_uuid])
                    if o_uuid:
                        nodes[c_uuid]['children'].append(
                            tools.offer_row_to_dict(*offer))
                root = nodes[unit_uuid]
                print("nodes tree construct & returning time: ", datetime.now() - start_time)
                return root
