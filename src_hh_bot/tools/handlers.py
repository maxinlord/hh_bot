import contextlib
import json
from datetime import datetime
from functools import wraps

import config
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, Message
from db import User, Value
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import tools


async def subscription_price(message: Message, session: AsyncSession, discount: int):
    price = await session.scalar(
        select(Value.value_int).where(Value.name == "subscription_price")
    )
    price = int(price * ((100 - discount) / 100)) if discount > 0 else price
    price = max(price, 80)
    tools.end_life_invoice_ = await tools.end_life_invoice()
    await message.answer_invoice(
        title=await tools.get_text_message("title_invoice"),
        description=await tools.get_text_message("description_invoice"),
        provider_token=config.PAY_TOKEN,
        currency="rub",
        prices=[
            LabeledPrice(
                label=await tools.get_text_message("label_invoice"), amount=price * 100
            )
        ],
        payload=f"{message.message_id+1}:{tools.end_life_invoice_}",
    )


def delete_markup(func):
    @wraps(func)
    async def wrapper(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        user: User,
        **kwargs,
    ):
        msg_id = (await state.get_data()).get("msg_id")
        if msg_id:
            with contextlib.suppress(Exception):
                await message.bot.edit_message_reply_markup(
                    chat_id=message.from_user.id,
                    message_id=msg_id,
                    reply_markup=None,
                )
        await func(message, state, session, user, **kwargs)

    return wrapper


async def save_viewing_form(state, user, session):
    data = await state.get_data()
    decoded_dict: dict = json.loads(user.last_idpk_form or "{}")
    key = data["tag"] or "__all"
    decoded_dict[key] = data["current_idpk"]
    user.last_idpk_form = json.dumps(decoded_dict, ensure_ascii=False)
    await session.commit()
    await state.clear()


async def save_user(session: AsyncSession, message: Message, user: User | None) -> User:
    if user:
        return user
    user = User(
        id_user=message.from_user.id,
        username=message.from_user.username
        or await tools.get_text_message("username_is_missing"),
        name=message.from_user.full_name,
        date_reg=datetime.now(),
    )
    session.add(user)
    await session.commit()
    return user
