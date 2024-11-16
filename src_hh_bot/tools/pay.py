from datetime import datetime, timedelta

from db import Value
from init_db import _sessionmaker_for_func
from sqlalchemy import select


async def end_life_invoice():
    async with _sessionmaker_for_func() as session:
        time_life_invoice = await session.scalar(
            select(Value.value_int).where(Value.name == "time_life_invoice")
        )
        end_life_invoice = datetime.now() + timedelta(seconds=time_life_invoice)
        end_life_invoice = end_life_invoice.strftime("%d.%m.%Y %H.%M.%S")
    return end_life_invoice
