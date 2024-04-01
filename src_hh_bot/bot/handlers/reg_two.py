from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.filters import GetTextButton
from bot.keyboards import Form
from db import User, Value
from tools import get_text_message, form_not_complete
from bot.keyboards import (
    k_form_fields,
    k_options_for_photo,
    k_main_menu,
    k_gen_bttn_tags,
    Tag,
)
from bot.states import FormTwoState


router = Router()


@router.callback_query(F.data == "reg_two")
async def menu_form_two(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    no_set = await get_text_message("not_set")
    data["field_1"] = no_set
    data["field_2"] = no_set
    data["field_3"] = no_set
    data["field_4"] = no_set
    data["field_5"] = no_set
    data["photos_id"] = list()
    await state.update_data(data)
    await query.message.edit_text(
        text=await get_text_message("form_two", **data),
        reply_markup=await k_form_fields(form_type="two"),
    )
    await state.set_state(FormTwoState.main)


@router.callback_query(FormTwoState.main, Form.filter(F.field == 1))
async def form_two_field_1(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_two_field_1"), reply_markup=None
    )
    await state.set_state(FormTwoState.field_1)


@router.message(FormTwoState.field_1, F.text)
async def get_form_two_field_1(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if len(message.text) > await session.scalar(
        select(Value.value_int).where(Value.name == "form_two_field_1_symbols")
    ):
        await message.answer(text=await get_text_message("max_length"))
        return
    data = await state.update_data(field_1=message.text)
    await message.answer(
        text=await get_text_message("form_two", **data),
        reply_markup=await k_form_fields(form_type="two"),
    )
    await state.set_state(FormTwoState.main)


@router.callback_query(FormTwoState.main, Form.filter(F.field == 2))
async def form_two_field_2(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_two_field_2"), reply_markup=None
    )
    await state.set_state(FormTwoState.field_2)


@router.message(FormTwoState.field_2, F.text)
async def get_form_two_field_2(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if len(message.text) > await session.scalar(
        select(Value.value_int).where(Value.name == "form_two_field_2_symbols")
    ):
        await message.answer(text=await get_text_message("max_length"))
        return
    data = await state.update_data(field_2=message.text)
    await message.answer(
        text=await get_text_message("form_two", **data),
        reply_markup=await k_form_fields(form_type="two"),
    )
    await state.set_state(FormTwoState.main)


@router.callback_query(FormTwoState.main, Form.filter(F.field == 3))
async def form_two_field_3(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_two_field_3"), reply_markup=None
    )
    await state.set_state(FormTwoState.field_3)


@router.message(FormTwoState.field_3, F.text)
async def get_form_two_field_3(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if len(message.text) > await session.scalar(
        select(Value.value_int).where(Value.name == "form_two_field_3_symbols")
    ):
        await message.answer(text=await get_text_message("max_length"))
        return
    data = await state.update_data(field_3=message.text)
    await message.answer(
        text=await get_text_message("form_two", **data),
        reply_markup=await k_form_fields(form_type="two"),
    )
    await state.set_state(FormTwoState.main)


@router.callback_query(FormTwoState.main, Form.filter(F.field == 4))
async def form_two_field_4(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_two_field_4"),
        reply_markup=await k_gen_bttn_tags(),
    )
    await state.set_state(FormTwoState.field_4)


@router.callback_query(FormTwoState.field_4, Tag.filter(F.type == "tag"))
async def get_form_two_field_4(
    query: CallbackQuery,
    state: FSMContext,
    callback_data: Tag,
    session: AsyncSession,
    user: User,
) -> None:
    data = await state.update_data(field_4=callback_data.value)
    await query.message.edit_text(
        text=await get_text_message("form_two", **data),
        reply_markup=await k_form_fields(form_type="two"),
    )
    await state.set_state(FormTwoState.main)


@router.callback_query(FormTwoState.main, Form.filter(F.field == 5))
async def form_two_field_5(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.delete()
    await query.message.answer(
        text=await get_text_message("form_two_field_5"),
        reply_markup=await k_options_for_photo(),
    )
    await state.set_state(FormTwoState.field_5)


@router.message(FormTwoState.field_5, F.photo)
async def get_photos_two(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    photos_id: list = data["photos_id"]
    if len(photos_id) >= await session.scalar(
        select(Value.value_int).where(Value.name == "num_of_photos")
    ):
        await message.answer(text=await get_text_message("max_photos"))
        return
    media_group = MediaGroupBuilder(caption=await get_text_message("u_can_send_more"))
    [media_group.add_photo(media=photo_id) for photo_id in photos_id]
    new_photo_id = message.photo[0].file_id
    photos_id.append(new_photo_id)
    await state.update_data(photos_id=photos_id)
    media_group.add_photo(media=new_photo_id)
    await message.answer_media_group(media=media_group.build())


@router.message(FormTwoState.field_5, GetTextButton("confirm"))
async def form_two_back(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    text = await get_text_message("field_5", quantity_photo=len(data["photos_id"]))
    data = await state.update_data(field_5=text)
    await message.answer(
        text=await get_text_message("back_to_form_two"),
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        text=await get_text_message("form_two", **data),
        reply_markup=await k_form_fields(form_type="two"),
    )
    await state.set_state(FormTwoState.main)


@router.message(FormTwoState.field_5, GetTextButton("clear_selected"))
async def form_two_clear_selected(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.update_data(field_5=0, photos_id=list())
    await message.answer(text=await get_text_message("cleaned_up"))


@router.callback_query(FormTwoState.main, F.data == "end_reg_two")
async def form_two_end_reg(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    if list_field_not_complete := await form_not_complete(
        data=data, field_to_skip=["field_5"], type_form="two"
    ):
        await query.answer(
            text=await get_text_message(
                "form_not_complete",
                list_field_not_complete=", ".join(list_field_not_complete),
            ),
            show_alert=True,
        )
        return
    user.form_type = "two"
    user.field_1 = data["field_1"]
    user.field_2 = data["field_2"]
    user.field_3 = data["field_3"]
    user.field_4 = data["field_4"]
    user.field_5 = ", ".join(data["photos_id"]) if len(data["photos_id"]) != 0 else None
    await session.commit()
    await state.clear()
    await query.message.edit_reply_markup(reply_markup=None)
    await query.message.answer(
        text=await get_text_message("form_complete"), reply_markup=await k_main_menu()
    )
