from datetime import datetime
from typing import Callable, Awaitable, Any
from tools import get_text_message
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import Value, Subscriptions
from bot.keyboards import k_subscribe


class CheckSubscription(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]
        if not await session.scalar(
            select(Value.value_int).where(Value.name == "subscribe_mode")
        ):
            return await handler(event, data)
        sub = await session.scalar(
            select(Subscriptions).where(Subscriptions.id_user == event.from_user.id)
        )
        if sub and datetime.now() < sub.date_end:
            return await handler(event, data)

        if isinstance(event, Message):
            if event.successful_payment:
                return await handler(event, data)
            if data.get("command") and data.get("command").args:
                return await handler(event, data)
            await event.answer(
                text=await get_text_message("no_subscription"),
                reply_markup=await k_subscribe(),
            )
        elif isinstance(event, CallbackQuery):
            if event.data == "sub":
                return await handler(event, data)
            await event.message.answer(
                text=await get_text_message("no_subscription"),
                reply_markup=await k_subscribe(),
            )
