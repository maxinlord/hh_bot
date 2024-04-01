from datetime import datetime
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db import User
from bot.filters import GetTextButton
from bot.states import FormOneState, FormTwoState
from tools import get_text_message, parser_ids_photo, delete_form
from bot.keyboards import (
    k_start_menu,
    k_types_of_reg,
    k_back,
    k_main_menu,
    k_my_form_menu,
    k_form_fields,
    k_confirm_del_form,
)


router = Router()


@router.message(GetTextButton("my_form"))
async def menu_my_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if user.field_5:
        await message.answer_media_group(media=parser_ids_photo(user.field_5))
    data = await state.get_data()
    data["field_1"] = user.field_1
    data["field_2"] = user.field_2
    data["field_3"] = user.field_3
    data["field_4"] = user.field_4
    data["photos_id"] = (
        list(map(lambda x: x.strip(), user.field_5.split(",")))
        if user.field_5
        else list()
    )
    data["field_5"] = (
        await get_text_message("field_5", quantity_photo=len(data["photos_id"]))
        if user.field_5
        else await get_text_message("field_5_skip_photo")
    )

    await state.update_data(data)
    await message.answer(
        text=await get_text_message("my_form", **data),
        reply_markup=await k_my_form_menu(),
    )


@router.message(GetTextButton("edit_my_form"))
async def edit_my_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    await message.answer(
        text=await get_text_message(f"form_{user.form_type}", **data),
        reply_markup=await k_form_fields(form_type=user.form_type),
    )
    match user.form_type:
        case "one":
            await state.set_state(FormOneState.main)
        case "two":
            await state.set_state(FormTwoState.main)


@router.message(GetTextButton("delete_my_form"))
async def delete_my_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("delete_my_form"),
        reply_markup=await k_confirm_del_form(),
    )


@router.message(GetTextButton("confirm_delete_form"))
async def confirm_delete_my_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await delete_form(idpk_user=user.idpk)
    await message.answer(
        text=await get_text_message("new_start", name_=message.from_user.full_name),
        reply_markup=await k_start_menu(),
    )


@router.message(GetTextButton("back"))
async def back_to_main_menu(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("my_form_menu"), reply_markup=await k_main_menu()
    )
