import asyncio

import aioschedule
import config
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.types import BotCommand
from bot.handlers import setup_message_routers
from bot.middlewares import CheckSubscription, CheckUser, DBSessionMiddleware
from db import Base
from init_db import _engine, _sessionmaker
from init_db_redis import redis
from jobs import update_last_idpk_form
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from tools import get_text_button

bot: Bot = Bot(
    config.BOT_TOKEN, parse_mode=ParseMode.HTML, disable_web_page_preview=True
)


async def on_startup(_engine: AsyncEngine) -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def on_shutdown(session: AsyncSession) -> None:
    await session.close_all()


async def scheduler() -> None:
    # aioschedule.every(1).seconds.do(job_sec)
    aioschedule.every().day.at("8:00").do(update_last_idpk_form)
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
    df = DefaultKeyBuilder(prefix="hh_bot")
    dp = Dispatcher(_engine=_engine, storage=RedisStorage(redis=redis, key_builder=df))

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.callback_query.middleware(DBSessionMiddleware(session_pool=_sessionmaker))

    dp.message.middleware(CheckUser())
    dp.callback_query.middleware(CheckUser())

    dp.message.middleware(CheckSubscription())
    dp.callback_query.middleware(CheckSubscription())

    message_routers = setup_message_routers()
    asyncio.create_task(scheduler())
    dp.include_router(message_routers)
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
