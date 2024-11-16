from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message
from db import BlackList, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CheckUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]
        if await session.scalar(
            select(BlackList).where(BlackList.id_user == event.from_user.id)
        ):
            return
        user = await session.scalar(
            select(User).where(User.id_user == event.from_user.id)
        )
        data["user"] = user
        return await handler(event, data)
