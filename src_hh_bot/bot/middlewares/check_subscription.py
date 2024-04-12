from datetime import datetime
from typing import Callable, Awaitable, Any
from tools import get_text_message
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import User, Subscriptions


class CheckSubscription(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]
        if await session.scalar(
            select(Subscriptions).where(Subscriptions.id_user == event.from_user.id)
        ):
            return await handler(event, data)

        if isinstance(event, Message):
            await event.answer(
                text=await get_text_message("no_subscription"), reply_markup=None
            )
        elif isinstance(event, CallbackQuery):
            await event.message.edit_reply_markup(reply_markup=None)
            await event.message.answer(
                text=await get_text_message("no_subscription"), reply_markup=None
            )
