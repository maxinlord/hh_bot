from sqlalchemy import select
from db import Text, Button, Value
from init_db import _sessionmaker_for_func


async def get_tags(name_tags: str = "tags_form_12") -> list:
    async with _sessionmaker_for_func() as session:
        tags_str = await session.scalar(
            select(Value.value_str).where(Value.name == name_tags)
        )
        tags_list = list(map(lambda x: x.strip(), tags_str.split(",")))
    return tags_list


async def get_num_column_for_tags(
    name_column_tags: str = "num_column_tags_form_12",
) -> int:
    async with _sessionmaker_for_func() as session:
        return await session.scalar(
            select(Value.value_int).where(Value.name == name_column_tags)
        )
