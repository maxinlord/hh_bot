from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db import User
from bot.filters import GetTextButton
from bot.states import FormOneState, FormTwoState, FormFourState, FormThreeState
from tools import (
    get_text_message,
    ids_to_media_group,
    delete_form,
    to_dict_form_fields,
    delete_markup,
    get_city,
)
from bot.keyboards import (
    k_start_menu,
    k_main_menu,
    k_my_form_menu,
    k_form_fields,
    k_confirm_del_form,
)


router = Router()
ADJUST_THREE = [2, 2, 2]
ADJUST_FOUR = [2, 2, 2]


@router.message(GetTextButton("my_form"))
async def menu_my_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    form_fields = await to_dict_form_fields(user.form_fields)
    if user.form_type in ["one", "two"]:
        for field in ["field_1", "field_2", "field_3", "field_4"]:
            data[field] = form_fields.get(field, "")
        data["photos_id"] = form_fields.get("field_5", [])

        data["field_5"] = (
            await get_text_message("field_5", quantity_photo=len(data["photos_id"]))
            if data["photos_id"]
            else await get_text_message("field_5_skip_photo")
        )
    elif user.form_type in ["three", "four"]:
        for field in [
            "field_1",
            "field_2",
            "field_3",
            "field_4",
            "field_5",
            "field_6",
            "city",
        ]:
            data[field] = form_fields.get(field, "")
    await state.update_data(data)

    await message.answer(
        text=await get_text_message("open_form", **data),
        reply_markup=await k_my_form_menu(),
    )

    if user.form_type in ["one", "two"] and data["photos_id"]:
        await message.answer_media_group(
            media=ids_to_media_group(
                data["photos_id"],
                caption=await get_text_message(f"my_form_{user.form_type}", **data),
            )
        )
    else:
        await message.answer(
            text=await get_text_message(f"my_form_{user.form_type}", **data)
        )


@router.message(GetTextButton("edit_my_form"))
@delete_markup
async def edit_my_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    match user.form_type:
        case "one":
            msg = await message.answer(
                text=await get_text_message(f"form_{user.form_type}", **data),
                reply_markup=await k_form_fields(form_type=user.form_type),
            )
            await state.set_state(FormOneState.main)
        case "two":
            msg = await message.answer(
                text=await get_text_message(f"form_{user.form_type}", **data),
                reply_markup=await k_form_fields(form_type=user.form_type),
            )
            await state.set_state(FormTwoState.main)
        case "three":
            msg = await message.answer(
                text=await get_text_message(f"form_{user.form_type}", **data),
                reply_markup=await k_form_fields(
                    form_type=user.form_type,
                    amount_fields=6,
                    adjust=ADJUST_THREE,
                    change_city=True,
                ),
            )
            await state.set_state(FormThreeState.main)
        case "four":
            msg = await message.answer(
                text=await get_text_message(f"form_{user.form_type}", **data),
                reply_markup=await k_form_fields(
                    form_type=user.form_type,
                    amount_fields=6,
                    adjust=ADJUST_FOUR,
                    change_city=True,
                ),
            )
            await state.set_state(FormFourState.main)
    await state.update_data(data)
    await state.update_data(msg_id=msg.message_id)


@router.message(GetTextButton("delete_my_form"))
@delete_markup
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
        text=await get_text_message("delete_my_form_success"),
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        text=await get_text_message("new_start", name_=message.from_user.full_name),
        reply_markup=await k_start_menu(),
    )


@router.message(GetTextButton("back"))
@delete_markup
async def back_to_main_menu(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("my_form_menu"), reply_markup=await k_main_menu()
    )


@router.message(GetTextButton("cancel"))
async def back_to_options(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("my_form_menu"),
        reply_markup=await k_my_form_menu(),
    )
