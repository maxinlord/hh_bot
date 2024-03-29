import asyncio
import aioschedule
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from aiogram.fsm.storage.redis import RedisStorage
from bot.handlers import setup_message_routers
from bot.middlewares import DBSessionMiddleware, CheckUser
from db import Base
from init_db import _sessionmaker, _engine
from init_db_redis import redis
import config
from tools import get_text_button

bot: Bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)


async def on_startup(_engine: AsyncEngine) -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def on_shutdown(session: AsyncSession) -> None:
    await session.close_all()


async def scheduler() -> None:
    # aioschedule.every(1).seconds.do(job_sec, bot=bot)
    # aioschedule.every().day.at("18:00").do(job_day, bot=bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(
                command="start", description=await get_text_button("command_start")
            ),
        ]
    )


async def main() -> None:

    dp = Dispatcher(_engine=_engine, storage=RedisStorage(redis=redis))

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.callback_query.middleware(DBSessionMiddleware(session_pool=_sessionmaker))

    dp.message.middleware(CheckUser())
    dp.callback_query.middleware(CheckUser())

    message_routers = setup_message_routers()
    asyncio.create_task(scheduler())
    dp.include_router(message_routers)
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
