import contextlib
import json
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db import User
from tools import (
    get_text_message,
    form_not_complete,
    is_city_exist,
    delete_markup,
    validate_input,
)
from bot.states import FormThreeState
from bot.keyboards import (
    Form,
    k_form_fields,
    ik_gen_tags_form_34,
    Tag,
    k_main_menu,
    k_back,
    k_types_of_reg,
)


router = Router()
ADJUST = [2, 2, 2]


@router.callback_query(F.data == "reg_three")
async def menu_form_three(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    msg = await query.message.edit_text(
        text=await get_text_message("form_three_enter_city"),
        reply_markup=await k_back(),
    )
    await state.set_state(FormThreeState.enter_city)
    await state.update_data(msg_id=msg.message_id)


@router.callback_query(FormThreeState.enter_city, F.data == "back")
async def menu_form_three_enter_city(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("select_type_registration"),
        reply_markup=await k_types_of_reg(),
    )


@router.message(FormThreeState.enter_city, F.text)
@delete_markup
async def get_form_three_enter_city(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    if not await is_city_exist(message.text):
        msg = await message.answer(
            text=await get_text_message("city_not_exist"),
            reply_markup=await k_back(),
        )
        await state.update_data(msg_id=msg.message_id)
        return
    no_set = await get_text_message("not_set")
    fields_to_update = [
        "field_1",
        "field_2",
        "field_3",
        "field_4",
        "field_5",
        "field_6",
    ]
    data["city"] = message.text.strip().capitalize()
    data.update({field: no_set for field in fields_to_update})
    await state.update_data(data)
    await message.answer(
        text=await get_text_message("form_three", **data),
        reply_markup=await k_form_fields(
            form_type="three", amount_fields=6, adjust=ADJUST
        ),
    )
    await state.set_state(FormThreeState.main)


@router.callback_query(FormThreeState.main, Form.filter(F.field == 1))
async def form_three_field_1(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_three_field_1"), reply_markup=None
    )
    await state.set_state(FormThreeState.field_1)


@router.message(FormThreeState.field_1, F.text)
async def get_form_three_field_1(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.update_data(field_1=message.text)
    await message.answer(
        text=await get_text_message("form_three", **data),
        reply_markup=await k_form_fields(
            form_type="three", amount_fields=6, adjust=ADJUST
        ),
    )
    await state.set_state(FormThreeState.main)


@router.callback_query(FormThreeState.main, Form.filter(F.field == 2))
async def form_three_field_2(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_three_field_2"), reply_markup=None
    )
    await state.set_state(FormThreeState.field_2)


@router.message(FormThreeState.field_2, F.text)
async def get_form_three_field_2(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.update_data(field_2=message.text)
    await message.answer(
        text=await get_text_message("form_three", **data),
        reply_markup=await k_form_fields(
            form_type="three", amount_fields=6, adjust=ADJUST
        ),
    )
    await state.set_state(FormThreeState.main)


@router.callback_query(FormThreeState.main, Form.filter(F.field == 3))
async def form_three_field_3(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_three_field_3"), reply_markup=None
    )
    await state.set_state(FormThreeState.field_3)


@router.message(FormThreeState.field_3, F.text)
async def get_form_three_field_3(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.update_data(field_3=message.text)
    await message.answer(
        text=await get_text_message("form_three", **data),
        reply_markup=await k_form_fields(
            form_type="three", amount_fields=6, adjust=ADJUST
        ),
    )
    await state.set_state(FormThreeState.main)


@router.callback_query(FormThreeState.main, Form.filter(F.field == 4))
async def form_three_field_4(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_three_field_4"), reply_markup=None
    )
    await state.set_state(FormThreeState.field_4)


@router.message(FormThreeState.field_4, F.text)
async def get_form_three_field_4(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if not validate_input(message.text):
        await message.answer(
            text=await get_text_message("form_three_field_4_error"),
            reply_markup=None,
        )
        return
    data = await state.update_data(field_4=message.text)
    await message.answer(
        text=await get_text_message("form_three", **data),
        reply_markup=await k_form_fields(
            form_type="three", amount_fields=6, adjust=ADJUST
        ),
    )
    await state.set_state(FormThreeState.main)


@router.callback_query(FormThreeState.main, Form.filter(F.field == 5))
async def form_three_field_5(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_three_field_5"), reply_markup=None
    )
    await state.set_state(FormThreeState.field_5)


@router.message(FormThreeState.field_5, F.entities[0].type == "url")
async def get_form_three_field_5(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    entity = message.entities[0]
    url = message.text[entity.offset : entity.offset + entity.length]
    data = await state.update_data(field_5=url)
    await message.answer(
        text=await get_text_message("form_three", **data),
        reply_markup=await k_form_fields(
            form_type="three", amount_fields=6, adjust=ADJUST
        ),
    )
    await state.set_state(FormThreeState.main)


@router.callback_query(FormThreeState.main, Form.filter(F.field == 6))
async def form_three_field_6(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(
        text=await get_text_message("form_three_field_6"),
        reply_markup=await ik_gen_tags_form_34(),
    )
    await state.set_state(FormThreeState.field_6)


@router.callback_query(FormThreeState.field_6, Tag.filter(F.type == "tag"))
async def get_form_three_field_6(
    query: CallbackQuery,
    state: FSMContext,
    callback_data: Tag,
    session: AsyncSession,
    user: User,
) -> None:
    data = await state.update_data(field_6=callback_data.value)
    await query.message.edit_text(
        text=await get_text_message("form_three", **data),
        reply_markup=await k_form_fields(
            form_type="three", amount_fields=6, adjust=ADJUST
        ),
    )
    await state.set_state(FormThreeState.main)


@router.callback_query(FormThreeState.main, F.data == "end_reg_three")
async def form_three_end_reg(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    if list_field_not_complete := await form_not_complete(data=data, field_to_skip=[]):
        await query.answer(
            text=await get_text_message(
                "form_not_complete",
                list_field_not_complete=", ".join(list_field_not_complete),
            ),
            show_alert=True,
        )
        return
    user.form_type = "three"
    form_fields = {
        "city": data["city"],
        "field_1": data["field_1"],
        "field_2": data["field_2"],
        "field_3": data["field_3"],
        "field_4": data["field_4"],
        "field_5": data["field_5"],
        "field_6": data["field_6"],
    }

    user.form_fields = json.dumps(form_fields)
    await session.commit()
    await state.clear()
    await query.message.edit_reply_markup(reply_markup=None)
    await query.message.answer(
        text=await get_text_message("form_complete"), reply_markup=await k_main_menu()
    )


@router.callback_query(FormThreeState.main, F.data == "change_city_three")
async def menu_form_three(
    query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await query.message.edit_text(text=await get_text_message("form_three_enter_city"))
    await state.set_state(FormThreeState.edit_enter_city)


@router.message(FormThreeState.edit_enter_city, F.text)
async def get_form_three_edit_enter_city(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if not await is_city_exist(message.text):
        await message.answer(text=await get_text_message("city_not_exist"))
        return
    data = await state.get_data()
    data["city"] = message.text.strip().capitalize()
    await state.update_data(data)
    await message.answer(
        text=await get_text_message("form_three", **data),
        reply_markup=await k_form_fields(
            form_type="three",
            amount_fields=6,
            adjust=ADJUST,
            change_city=True,
        ),
    )
    await state.set_state(FormThreeState.main)
