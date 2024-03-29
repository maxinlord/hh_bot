from sqlalchemy import select
from db import Photo
from init_db import _sessionmaker_for_func


async def get_id_photo(name: str) -> str:
    async with _sessionmaker_for_func() as session:
        photo_id = await session.scalar(select(Photo.photo_id).where(Photo.name == name))
        return photo_id