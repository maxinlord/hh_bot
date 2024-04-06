from aiogram import Bot
from sqlalchemy import select, update
from db import User
from init_db import _sessionmaker_for_func


async def job_sec(bot: Bot) -> None:
    pass


async def job_minute() -> None:
    pass


async def update_last_idpk_form() -> None:
    async with _sessionmaker_for_func() as session:
        await session.execute(
            update(User).where(User.last_idpk_form != None).values(last_idpk_form=None)
        )
        await session.commit()
