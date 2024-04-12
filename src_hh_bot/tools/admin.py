from sqlalchemy import select
from db import User, Value
from init_db import _sessionmaker_for_func


async def get_id_admin() -> int:
    async with _sessionmaker_for_func() as session:
        id_admin = await session.scalar(
            select(Value.value_str).where(Value.name == "id_admin")
        )
        return int(id_admin)
