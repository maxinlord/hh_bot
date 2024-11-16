from db import Value
from init_db import _sessionmaker_for_func
from sqlalchemy import select


async def get_id_admin() -> int:
    async with _sessionmaker_for_func() as session:
        id_admin = await session.scalar(
            select(Value.value_str).where(Value.name == "id_admin")
        )
        return int(id_admin)
