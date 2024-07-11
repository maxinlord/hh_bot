from datetime import datetime, timedelta
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import User, PromoCode, Subscriptions
from tools import get_text_message, subscription_price
from bot.keyboards import k_start_menu, k_types_of_reg, k_back, k_main_menu
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

router = Router()


@router.message(CommandStart(deep_link=True))
async def handler(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    state: FSMContext,
    user: User | None,
):
    new_user = False
    # проверяем есть ли пользователь в базе данных
    if not user:
        user = User(
            id_user=message.from_user.id,
            username=message.from_user.username
            or await get_text_message("username_is_missing"),
            name=message.from_user.full_name,
            date_reg=datetime.now(),
        )
        session.add(user)
        new_user = True

    # проверяем есть ли такой промокод в базе данных
    promocode = await session.scalar(
        select(PromoCode).where(PromoCode.code == command.args)
    )
    if not promocode:
        return await message.answer(
            text=await get_text_message("deep_link_promocode_not_found")
        )

    # проверяем есть ли такой промокод в списке активированных промокодов
    # или есть ли такая подписка с таким промокодом
    data = await state.get_data()
    activated_promocode = await session.scalar(
        select(Subscriptions.plan).where(
            Subscriptions.plan == f"promocode_{promocode.code}"
        )
    )
    pressed_promocodes: list = data.get("pressed_promocodes", [])
    if (promocode.code in pressed_promocodes) or activated_promocode:
        await message.answer(text=await get_text_message("deep_link_promocode_pressed"))
        return
    pressed_promocodes.append(promocode.code)

    # проверяем есть ли закончились триггеры для данного промокода
    if (
        promocode.num_enable_triggers > 0
        and promocode.num_enable_triggers == promocode.num_activated
    ):
        return await message.answer(
            text=await get_text_message("deep_link_promocode_end")
        )

    sub_data = {
        "plan": f"promocode_{promocode.code}",
        "days_sub": promocode.days_sub,
        "new_user": new_user,
    }
    promocode.num_activated += 1
    await state.update_data(
        promocode_sub=sub_data, pressed_promocodes=pressed_promocodes
    )

    # если скидка промокода равна 100% то делаем подписку на бесплатный план,
    # либо продлеваем если есть подписка
    sub_free = False
    if promocode.discount == 100:
        days = promocode.days_sub if promocode.days_sub > 0 else 365 * 10
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
        await message.answer(
            text=await get_text_message("deep_link_promocode_free_pay")
        )

        # если пользователь новый то отправляем ему главное меню
        if new_user:
            await state.clear()
            await message.answer(
                text=await get_text_message("start", name_=message.from_user.full_name),
                reply_markup=await k_start_menu(),
            )
        return

    # если скидка промокода не равна 100% то делаем счет на оплату подписки
    await session.commit()
    await subscription_price(
        message=message, discount=promocode.discount, session=session
    )


@router.message(CommandStart(), StateFilter(default_state))
async def command_start(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None,
) -> None:
    await state.clear()
    if not user:
        user = User(
            id_user=message.from_user.id,
            username=message.from_user.username
            or await get_text_message("username_is_missing"),
            name=message.from_user.full_name,
            date_reg=datetime.now(),
        )
        session.add(user)
        await session.commit()
    if not user.form_type:
        await message.answer(
            text=await get_text_message("start", name_=message.from_user.full_name),
            reply_markup=await k_start_menu(),
        )
        return
    await message.answer(
        text=await get_text_message("main_menu"), reply_markup=await k_main_menu()
    )


@router.callback_query(F.data == "select_reg")
async def process_select_reg(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("select_type_registration"),
        reply_markup=await k_types_of_reg(),
    )


@router.callback_query(F.data == "pre_reg_info")
async def process_pre_reg_info(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("pre_reg_info"), reply_markup=await k_back()
    )


@router.callback_query(StateFilter(default_state), F.data == "back")
async def process_back(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("start", name_=query.from_user.full_name),
        reply_markup=await k_start_menu(),
    )
