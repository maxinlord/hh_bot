from sqlalchemy import select
from db import Text, Button, Value
from init_db import _sessionmaker_for_func

async def get_tags() -> list:
    async with _sessionmaker_for_func() as session:
        tags_str = await session.scalar(select(Value.value_str).where(Value.name == 'tags'))
        tags_list = list(map(lambda x: x.strip(), tags_str.split(',')))
    return tags_list

async def get_num_column_for_tags() -> int:
    async with _sessionmaker_for_func() as session:
        return await session.scalar(select(Value.value_int).where(Value.name == 'num_column_for_tags'))