from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import create_start_link
from bot.keyboards import (
    Ban,
    k_promocode_menu,
)
from bot.states import Admin
from db import BlackList, PromoCode, User
from sqlalchemy.ext.asyncio import AsyncSession
from tools import (
    filter_by_keys,
    gen_id_promocode,
    get_id_admin,
    get_text_message,
    mention_html,
)

router = Router()


@router.callback_query(Ban.filter(F.type == "ban"))
async def answ_report(
    query: CallbackQuery,
    callback_data: Ban,
    state: FSMContext,
    session: AsyncSession,
    user: User,
) -> None:
    user_to_ban = await session.get(User, callback_data.idpk_user)
    session.add(BlackList(id_user=user_to_ban.id_user))
    await session.commit()
    await query.message.edit_text(
        text=await get_text_message(
            "user_banned",
            id_user=user_to_ban.id_user,
            link_on_user=mention_html(
                id_user=user_to_ban.id_user, name=user_to_ban.name
            ),
        )
    )


@router.message(Command("promocode"))
async def menu_promocode(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if not (user.id_user == await get_id_admin()):
        return
    await message.answer(
        text=await get_text_message("menu_promocode"),
        reply_markup=await k_promocode_menu(),
    )
    await state.set_state(Admin.main)


@router.callback_query(Admin.main, F.data == "discount")
async def set_discount(
    query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
) -> None:
    await query.message.edit_text(
        text=await get_text_message("enter_discount"), reply_markup=None
    )
    await state.set_state(Admin.get_discount)


@router.message(Admin.get_discount)
async def get_discount(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if not message.text.isdigit():
        await message.answer(text=await get_text_message("not_digit"))
        return
    discount = int(message.text)
    if discount > 100:
        await message.answer(text=await get_text_message("discount_more_100"))
        return
    if discount < 0:
        await message.answer(text=await get_text_message("discount_less_0"))
        return
    data = await state.get_data()
    additional_text: dict = data.get("additional_text", {})
    additional_text["discount"] = await get_text_message(
        "discount_set", discount=discount
    )
    await state.update_data(discount=discount, additional_text=additional_text)
    await state.set_state(Admin.main)
    await message.answer(
        text=await get_text_message("menu_promocode")
        + "\n"
        + "\n".join(additional_text.values()),
        reply_markup=await k_promocode_menu(),
    )


@router.callback_query(Admin.main, F.data == "days_sub")
async def set_days_sub(
    query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
) -> None:
    await query.message.edit_text(
        text=await get_text_message("enter_days_sub"), reply_markup=None
    )
    await state.set_state(Admin.get_days_sub)


@router.message(Admin.get_days_sub)
async def get_days_sub(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if not message.text.isdigit():
        await message.answer(text=await get_text_message("not_digit"))
        return
    days_sub = int(message.text)
    if days_sub < 0:
        await message.answer(text=await get_text_message("days_sub_less_0"))
        return
    data = await state.get_data()
    additional_text: dict = data.get("additional_text", {})
    additional_text["days_sub"] = await get_text_message(
        "days_sub_set", days_sub=days_sub
    )
    await state.update_data(days_sub=days_sub, additional_text=additional_text)
    await state.set_state(Admin.main)
    await message.answer(
        text=await get_text_message("menu_promocode")
        + "\n"
        + "\n".join(additional_text.values()),
        reply_markup=await k_promocode_menu(),
    )


@router.callback_query(Admin.main, F.data == "num_enable_triggers")
async def set_num_enable_triggers(
    query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
) -> None:
    await query.message.edit_text(
        text=await get_text_message("enter_num_enable_triggers"), reply_markup=None
    )
    await state.set_state(Admin.get_num_enable_triggers)


@router.message(Admin.get_num_enable_triggers)
async def get_num_enable_triggers(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if not message.text.isdigit():
        await message.answer(text=await get_text_message("not_digit"))
        return
    num_enable_triggers = int(message.text)
    if num_enable_triggers <= 0:
        await message.answer(text=await get_text_message("num_enable_triggers_less_0"))
        return
    data = await state.get_data()
    additional_text: dict = data.get("additional_text", {})
    additional_text["num_enable_triggers"] = await get_text_message(
        "num_enable_triggers_set", num_enable_triggers=num_enable_triggers
    )
    await state.update_data(
        num_enable_triggers=num_enable_triggers, additional_text=additional_text
    )
    await state.set_state(Admin.main)
    await message.answer(
        text=await get_text_message("menu_promocode")
        + "\n"
        + "\n".join(additional_text.values()),
        reply_markup=await k_promocode_menu(),
    )


@router.callback_query(Admin.main, F.data == "gen_link")
async def gen_link(
    query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
) -> None:
    data = await state.get_data()
    data["code"] = gen_id_promocode(len_=12)
    session.add(
        PromoCode(
            **filter_by_keys(
                d=data,
                keys=[
                    "code",
                    "discount",
                    "days_sub",
                    "num_enable_triggers",
                    "num_activated",
                ],
            )
        )
    )
    await session.commit()
    link_promocode = await create_start_link(query.bot, data["code"])
    await query.message.delete_reply_markup()
    await query.message.answer(
        text=await get_text_message(
            "gen_link_promocode", link_promocode=link_promocode
        ),
        reply_markup=None,
    )
    await state.clear()
