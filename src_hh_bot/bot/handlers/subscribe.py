import contextlib
from datetime import datetime, timedelta
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from db import User, Value, Subscriptions
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tools import get_text_message, end_life_invoice
from bot.keyboards import k_start_menu
import config

router = Router()

DAYS_IN_YEAR = 365
YEARS = 10
ALL_DAYS = DAYS_IN_YEAR * YEARS


@router.callback_query(F.data == "sub")
async def subscribe(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
):
    price = await session.scalar(
        select(Value.value_int).where(Value.name == "subscription_price")
    )
    end_life_invoice_ = await end_life_invoice()
    await query.message.delete_reply_markup()
    await query.message.answer_invoice(
        title=await get_text_message("title_invoice"),
        description=await get_text_message("description_invoice"),
        provider_token="",
        currency="XTR",
        prices=[
            LabeledPrice(
                label=await get_text_message("label_invoice"), amount=price
            )
        ],
        payload=f"{query.message.message_id+1}:{end_life_invoice_}",
    )


@router.pre_checkout_query()
async def answ_on_buy(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    message_id, end_life_invoice = pre_checkout_query.invoice_payload.split(":")
    if datetime.now() > datetime.strptime(end_life_invoice, "%d.%m.%Y %H.%M.%S"):
        await pre_checkout_query.answer(
            ok=False, error_message=await get_text_message("error_time_life_invoice")
        )
        await pre_checkout_query.bot.delete_message(
            chat_id=pre_checkout_query.from_user.id, message_id=message_id
        )
        return
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(
    message: Message, user: User, session: AsyncSession, state: FSMContext
):
    message_id, _ = message.successful_payment.invoice_payload.split(":")
    with contextlib.suppress(Exception):
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message_id)

    # если в данных состояния есть данные о промо подписке тогда активируем ее
    data = await state.get_data()
    if sub_data := data.get("promocode_sub"):
        days = sub_data["days_sub"] if sub_data["days_sub"] > 0 else ALL_DAYS
        date_end = datetime.now() + timedelta(days=days)
        if sub := await session.scalar(
            select(Subscriptions).where(Subscriptions.id_user == user.id_user)
        ):
            sub.plan = sub_data["plan"]
            sub.date_end += timedelta(days=days)
        else:
            session.add(
                Subscriptions(
                    id_user=user.id_user,
                    plan=sub_data["plan"],
                    date_end=date_end,
                    date_start=datetime.now(),
                )
            )
        await session.commit()
        await message.answer(text=await get_text_message("successful_payment"))

        # если пользователь новый то отправляем ему главное меню
        if sub_data["new_user"]:
            await message.answer(
                text=await get_text_message("start", name_=message.from_user.full_name),
                reply_markup=await k_start_menu(),
            )
        return
    subscription_period = await session.scalar(
        select(Value.value_int).where(Value.name == "subscription_period")
    )
    date_start = datetime.now()
    date_end = date_start + timedelta(days=subscription_period)
    plan = "monthly"
    if sub := await session.scalar(
        select(Subscriptions).where(Subscriptions.id_user == user.id_user)
    ):
        sub.plan = plan
        sub.date_start = date_start
        sub.date_end = date_end
    else:
        session.add(
            Subscriptions(
                id_user=user.id_user,
                plan=plan,
                date_start=date_start,
                date_end=date_end,
            )
        )
    await state.clear()
    await session.commit()
    await message.answer(text=await get_text_message("successful_payment"))
