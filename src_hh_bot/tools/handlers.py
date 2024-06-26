import contextlib
from datetime import datetime, timedelta
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from db import User, Value, Subscriptions
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tools import get_text_message, end_life_invoice
import config


async def subscription_price(message: Message, session: AsyncSession, discount: int):
    price = await session.scalar(
        select(Value.value_int).where(Value.name == "subscription_price")
    )
    price = int(price * ((100 - discount) / 100)) if discount > 0 else price
    price = max(price, 80)
    end_life_invoice_ = await end_life_invoice()
    await message.answer_invoice(
        title=await get_text_message("title_invoice"),
        description=await get_text_message("description_invoice"),
        provider_token=config.PAY_TOKEN,
        currency="rub",
        prices=[
            LabeledPrice(
                label=await get_text_message("label_invoice"), amount=price * 100
            )
        ],
        payload=f"{message.message_id+1}:{end_life_invoice_}",
    )
